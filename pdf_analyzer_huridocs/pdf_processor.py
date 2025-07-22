import requests
import json
import os
import argparse
import re # Still imported, but specific regexes for H1/H2/H3 are removed from main logic

# --- Configuration ---
HURIDOCS_API_URL = "http://localhost:5060/"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# --- Helper Function: Ensure Directories Exist ---
def ensure_directories_exist():
    """Ensures input and output directories exist, creating them if necessary."""
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"Ensured '{INPUT_FOLDER}/' and '{OUTPUT_FOLDER}/' directories exist.")

# --- Function to Call HURIDOCS ---
def call_huridocs_api(pdf_path: str) -> list:
    """
    Sends a PDF file to the local HURIDOCS service and returns the parsed JSON output (list of segments).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Error: PDF file not found at: {pdf_path}")

    print(f"Sending '{os.path.basename(pdf_path)}' to HURIDOCS service at {HURIDOCS_API_URL}...")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            response = requests.post(HURIDOCS_API_URL, files=files, data={'fast': 'true'})
            response.raise_for_status()
            print("Successfully received response from HURIDOCS.")
            return response.json()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to HURIDOCS service at {HURIDOCS_API_URL}.")
        print("Please ensure the HURIDOCS Docker container is running (check 'docker ps').")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error from HURIDOCS: {e}")
        print(f"Response content: {response.text}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from HURIDOCS response for {os.path.basename(pdf_path)}.")
        print(f"Raw response: {response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during HURIDOCS API call for {os.path.basename(pdf_path)}: {e}")
        return None

# --- Function to Analyze Font Sizes ---
def analyze_font_sizes(segments: list) -> dict:
    """
    Analyzes all segments to determine font size thresholds for header classification.
    Returns a dictionary with size thresholds for different header levels.
    """
    # Collect all section headers and their font sizes
    header_sizes = []
    title_sizes = []
    
    for segment in segments:
        if segment.get("type") == "Section header":
            height = segment.get("height", 0)
            if height > 0:
                header_sizes.append(height)
        elif segment.get("type") == "Title":
            height = segment.get("height", 0)
            if height > 0:
                title_sizes.append(height)
    
    # If we have title sizes, use the largest as reference
    if title_sizes:
        max_title_size = max(title_sizes)
    else:
        max_title_size = max(header_sizes) if header_sizes else 15
    
    # Sort header sizes in descending order to establish hierarchy
    unique_sizes = sorted(set(header_sizes), reverse=True)
    
        # Establish thresholds based on the distinct font sizes found.
    if len(unique_sizes) >= 3:
        # More than 3 sizes, so we can define H1, H2, H3 clearly
        thresholds = {
            'title_threshold': max_title_size,
            'h1_threshold': unique_sizes[1],  # Largest size is H1
            'h2_threshold': unique_sizes[2],  # Second largest is H2
            'h3_threshold': unique_sizes[3],  # Third largest is H3
            'min_header_size': min(header_sizes) if header_sizes else 8
        }
    elif len(unique_sizes) == 2:
        # Only 2 sizes, map to H1 and H2
        thresholds = {
            'title_threshold': max_title_size,
            'h1_threshold': unique_sizes[1],
            'h2_threshold': unique_sizes[2],
            'h3_threshold': unique_sizes[3] - 1, # Fallback for smaller text
            'min_header_size': min(header_sizes) if header_sizes else 8
        }
    else:
        # Only one size, everything is H1
        thresholds = {
            'title_threshold': max_title_size,
            'h1_threshold': unique_sizes[0] if unique_sizes else 12.9,
            'h2_threshold': unique_sizes[0] - 1 if unique_sizes else 10.9,
            'h3_threshold': unique_sizes[0] - 2 if unique_sizes else 9.9,
            'min_header_size': min(header_sizes) if header_sizes else 8
        }
    
    return thresholds

# --- Function to Classify Header Level (Enhanced with Font Size) ---
def classify_header_level(text: str, page_num: int, font_height: float, thresholds: dict, is_after_title: bool = True) -> str:
    """
    Classifies a section header into H1, H2, or H3 based on font size and other heuristics.
    """
    # Use a small tolerance for floating point comparisons
    tolerance = 0.1
    
    # Primary classification based on font size
    if font_height >= thresholds['h1_threshold'] - tolerance:
        return "H1"
    elif font_height >= thresholds['h2_threshold'] - tolerance:
        return "H2"
    elif font_height >= thresholds['h3_threshold'] - tolerance:
        return "H3"
    
    # Fallback to content-based heuristics for edge cases
    text_length = len(text.strip())
    
    # Very short texts (like "?", single words) are likely H3
    if text_length <= 3:
        return "H3"
    
    # Email addresses are typically author info (H2)
    if "@" in text and "." in text:
        return "H2"
    
    # Check if it contains question words - likely H2
    question_words = ["what", "why", "how", "when", "where", "which", "who"]
    if any(word in text.lower() for word in question_words):
        return "H2"
    
    # Check if it's a step or numbered item - likely H2
    if re.match(r'^(step\s+\d+|chapter\s+\d+|\d+\.)', text.lower().strip()):
        return "H2"
    
    # Default based on font size tier
    if font_height > thresholds['min_header_size']:
        return "H2"
    else:
        return "H3"

# --- Function to Organize Document Outline (Enhanced with Font-Based Classification) ---
def organize_document_outline(huridocs_segments: list) -> dict:
    """
    Processes HURIDOCS segments to extract the main title and classify section headers 
    into H1, H2, H3 based on font size and content heuristics.
    """
    document_title = "Untitled Document"
    outline_items = []

    # Sort segments by page number and then top-left corner for robust reading order
    huridocs_segments.sort(key=lambda s: (s['page_number'], s['top'], s['left']))

    # Analyze font sizes to establish thresholds
    font_thresholds = analyze_font_sizes(huridocs_segments)
    print(f"Font size thresholds: {font_thresholds}")

    title_found = False
    section_headers = []

    # First pass: collect all section headers and titles
    for i, segment in enumerate(huridocs_segments):
        segment_type = segment["type"]
        text = segment["text"].strip()
        page_num = segment["page_number"]
        font_height = segment.get("height", 0)

        if not text:
            continue

        # --- Extract Main Document Title ---
        if segment_type == "Title" and not title_found:
            document_title = text
            title_found = True
            continue 

        # --- Collect Section Headers ---
        if segment_type == "Section header":
            section_headers.append({
                "text": text,
                "page": page_num,
                "height": font_height,
                "index": i
            })

    # If no title was found, look for the largest section header on page 1
    if not title_found and section_headers:
        # Find the section header with the largest font size on page 1
        page_1_headers = [h for h in section_headers if h["page"] == 1]
        if page_1_headers:
            largest_header = max(page_1_headers, key=lambda h: (h["height"], len(h["text"])))
            # Use the largest header as title if it's significantly larger than others or first on page
            document_title = largest_header["text"]
            title_found = True
            # Remove this header from section_headers
            section_headers = [h for h in section_headers if not (
                h["text"] == largest_header["text"] and 
                h["page"] == largest_header["page"] and
                h["height"] == largest_header["height"]
            )]

    # Second pass: classify remaining section headers using font size
    for header in section_headers:
        text = header["text"]
        page_num = header["page"]
        font_height = header["height"]
        index = header["index"]
        
        # Classify the header level using font-based approach
        level = classify_header_level(text, page_num, font_height, font_thresholds, is_after_title=title_found)
        
        outline_items.append({
            "level": level,
            "text": text,
            "page": page_num
        })

    return {
        "title": document_title,
        "outline": outline_items
    }

# --- Main Execution Logic ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processes all PDF files in the 'input' folder using the local "
                    "HURIDOCS layout analysis service and generates a structured JSON outline."
    )
    args = parser.parse_args() # Parses any potential arguments (currently none expected)

    ensure_directories_exist()

    pdf_files_to_process = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.pdf')]

    if not pdf_files_to_process:
        print(f"No PDF files found in the '{INPUT_FOLDER}' folder.")
        print("Please place your PDF files into this directory to process them.")
    else:
        print(f"Found {len(pdf_files_to_process)} PDF(s) to process in '{INPUT_FOLDER}'.")
        for pdf_filename in pdf_files_to_process:
            full_pdf_path = os.path.join(INPUT_FOLDER, pdf_filename)
            print(f"\n--- Processing: {pdf_filename} ---")

            huridocs_response_list = call_huridocs_api(full_pdf_path)

            if isinstance(huridocs_response_list, list) and huridocs_response_list:
                final_structured_output = organize_document_outline(huridocs_response_list)

                output_filename = os.path.splitext(pdf_filename)[0] + "_outline.json"
                output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)

                try:
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        json.dump(final_structured_output, f, indent=4, ensure_ascii=False)
                    print(f"Structured outline for '{pdf_filename}' saved to: {output_filepath}")
                except Exception as e:
                    print(f"Error saving structured outline JSON for '{pdf_filename}': {e}")
            else:
                print(f"HURIDOCS response for '{pdf_filename}' was not a valid list of segments or was empty. Skipping outline generation.")
                if huridocs_response_list is not None:
                    print(f"Received unexpected response type: {type(huridocs_response_list)}. Content: {huridocs_response_list}")

    print("\nAll PDF(s) processed (or attempted).")