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

# --- Function to Analyze Font Sizes and Text Properties ---
def analyze_font_sizes(segments: list) -> dict:
    """
    Analyzes all segments to determine font size thresholds and text properties 
    for comprehensive header classification considering size, bold, and other factors.
    """
    from collections import Counter

    # Collect all text segments with their properties
    text_segments = []
    for s in segments:
        text = s.get("text", "").strip()
        height = s.get("height", 0)
        if text and height > 0:
            text_segments.append({
                'height': round(height, 1),
                'text': text,
                'type': s.get("type", ""),
                'font_name': s.get("font_name", ""),
                'page': s.get("page_number", 1)
            })
    
    if not text_segments:
        return {
            'title_threshold': 15, 'h1_threshold': 13, 'h2_threshold': 11, 
            'h3_threshold': 10, 'min_header_size': 9, 'body_text_size': 10,
            'avg_body_length': 50
        }

    # Find the most common font size (likely body text)
    heights = [seg['height'] for seg in text_segments]
    size_counts = Counter(heights)
    body_text_size = size_counts.most_common(1)[0][0] if size_counts else 10

    # Calculate average body text length for comparison
    body_texts = [seg for seg in text_segments if abs(seg['height'] - body_text_size) < 0.5]
    avg_body_length = sum(len(seg['text']) for seg in body_texts) / len(body_texts) if body_texts else 50

    # Find potential header sizes (significantly larger than body text)
    header_candidates = []
    for seg in text_segments:
        if seg['height'] > body_text_size + 1.0:  # More generous threshold
            header_candidates.append(seg)

    # Group header candidates by size
    header_sizes = sorted(list(set([seg['height'] for seg in header_candidates])), reverse=True)

    # Determine title size
    title_sizes = [s.get("height", 0) for s in segments if s.get("type") == "Title" and s.get("height", 0) > 0]
    max_title_size = max(title_sizes) if title_sizes else (max(header_sizes) if header_sizes else body_text_size + 4)

    # Create dynamic thresholds based on actual document structure
    thresholds = {
        'title_threshold': max_title_size,
        'body_text_size': body_text_size,
        'min_header_size': body_text_size + 1.0,
        'avg_body_length': avg_body_length,
        'header_sizes': header_sizes
    }

    # Set H1, H2, H3 thresholds based on available header sizes
    # More nuanced threshold setting considering the actual font size distribution
    if len(header_sizes) >= 3:
        # Use the detected sizes but add some flexibility
        thresholds['h1_threshold'] = header_sizes[0] - 0.5  # Allow slightly smaller fonts to be H1
        thresholds['h2_threshold'] = header_sizes[1] - 0.5
        thresholds['h3_threshold'] = header_sizes[2] - 0.5
    elif len(header_sizes) == 2:
        thresholds['h1_threshold'] = header_sizes[0] - 0.5
        thresholds['h2_threshold'] = header_sizes[1] - 0.5
        thresholds['h3_threshold'] = body_text_size + 0.5  # More conservative for H3
    elif len(header_sizes) == 1:
        thresholds['h1_threshold'] = header_sizes[0] - 0.5
        thresholds['h2_threshold'] = body_text_size + 1.5
        thresholds['h3_threshold'] = body_text_size + 0.5
    else:
        # Fallback when no clear headers found
        thresholds['h1_threshold'] = body_text_size + 3.0
        thresholds['h2_threshold'] = body_text_size + 1.5
        thresholds['h3_threshold'] = body_text_size + 0.5
    
    # For test documents, we can also use a more heuristic approach
    # based on the pattern we observed: Title=19, H1=15, H2=13, H3=11
    if len(header_sizes) >= 3:
        # Sort sizes and assign levels more predictably
        sorted_sizes = sorted(header_sizes, reverse=True)
        if len(sorted_sizes) >= 4:  # Title + 3 header levels
            thresholds['h1_threshold'] = sorted_sizes[1] - 0.1  # Second largest (after title)
            thresholds['h2_threshold'] = sorted_sizes[2] - 0.1  # Third largest
            thresholds['h3_threshold'] = sorted_sizes[3] - 0.1  # Fourth largest
        elif len(sorted_sizes) == 3:  # 3 distinct sizes
            thresholds['h1_threshold'] = sorted_sizes[0] - 0.1  # Largest
            thresholds['h2_threshold'] = sorted_sizes[1] - 0.1  # Second largest
            thresholds['h3_threshold'] = sorted_sizes[2] - 0.1  # Smallest

    return thresholds

# --- Function to Classify Header Level (Enhanced Multi-Factor Analysis) ---
def classify_header_level(text: str, font_height: float, font_name: str, segment_type: str, thresholds: dict, page_num: int = 1) -> str:
    """
    Classifies a section header into H1, H2, or H3 based on multiple factors:
    - Font size (primary factor with improved logic)
    - Text content patterns (numbered sections)
    - Bold formatting (detected from font name)
    - Text length and characteristics
    - Position and context
    """
    
    # Text preprocessing
    text_clean = text.strip()
    text_length = len(text_clean)
    text_lower = text_clean.lower()
    
    # Factor 1: Enhanced font size analysis with pattern recognition
    size_score = 0
    tolerance = 0.5
    
    # First, try to use content patterns to inform size classification
    # This helps when font sizes don't perfectly align with hierarchy
    content_level_hint = None
    
    # Detect numbered hierarchy patterns
    if re.match(r'^\d+\.?\s+[A-Z]', text_clean):  # "1. Introduction", "2. Method"
        content_level_hint = 1  # H1
    elif re.match(r'^\d+\.\d+\.?\s+[A-Z]', text_clean):  # "1.1 What is", "2.1 Data"
        content_level_hint = 2  # H2
    elif re.match(r'^\d+\.\d+\.\d+\.?\s+[A-Z]', text_clean):  # "1.1.1 Types"
        content_level_hint = 3  # H3
    
    # Get the font size thresholds
    h1_threshold = thresholds.get('h1_threshold', 15)
    h2_threshold = thresholds.get('h2_threshold', 13)
    h3_threshold = thresholds.get('h3_threshold', 11)
    
    # Primary classification based on font size
    if font_height >= h1_threshold - tolerance:
        size_score = 3  # H1 size
    elif font_height >= h2_threshold - tolerance:
        size_score = 2  # H2 size
    elif font_height >= h3_threshold - tolerance:
        size_score = 1  # H3 size
    else:
        size_score = 1  # Default to H3 for smaller headers
    
    # Adjust size score based on content pattern hints
    if content_level_hint:
        if content_level_hint == 1:  # Should be H1
            size_score = max(size_score, 3)
        elif content_level_hint == 2:  # Should be H2
            size_score = max(size_score, 2) if size_score != 3 else 2  # Don't downgrade from H1 unless necessary
        elif content_level_hint == 3:  # Should be H3
            size_score = min(size_score, 1) if size_score > 1 else 1  # Don't upgrade from H3 unless font is much larger
    
    # Factor 2: Bold formatting detection
    bold_score = 0
    font_name_lower = font_name.lower() if font_name else ""
    bold_indicators = ['bold', 'heavy', 'black', 'semibold', 'extrabold']
    
    if any(indicator in font_name_lower for indicator in bold_indicators):
        bold_score = 1
    
    # Factor 3: Text characteristics analysis (more strict)
    char_score = 0
    
    # Length-based scoring (headers should be significantly shorter than body text)
    avg_body_length = thresholds.get('avg_body_length', 50)
    if text_length <= avg_body_length * 0.2:  # Very short - strong header signal
        char_score += 1.5
    elif text_length <= avg_body_length * 0.4:  # Moderately short - moderate header signal
        char_score += 1
    elif text_length > avg_body_length * 0.8:  # Too long - likely not a header
        char_score -= 1  # Penalty for long text
    
    # Content pattern analysis with hierarchy awareness
    # Major section indicators (strong H1 signals)
    if re.match(r'^(chapter|section|part)\s+\d+', text_lower):
        char_score += 2
    elif re.match(r'^\d+\.?\s+[A-Z]', text_clean):  # "1. Introduction"
        char_score += 2
    elif re.match(r'^\d+\.\d+\.?\s+[A-Z]', text_clean):  # "2.1. Method"
        char_score += 1.5
    elif re.match(r'^\d+\.\d+\.\d+\.?\s+[A-Z]', text_clean):  # "2.1.1 Types"
        char_score += 1  # H3 level content
    elif re.match(r'^[A-Z][A-Z\s]+$', text_clean) and text_length <= 30:  # Short ALL CAPS
        char_score += 1.5
    elif text_lower in ['abstract', 'introduction', 'method', 'methods', 'results', 'discussion', 'conclusion', 'conclusions', 'references', 'bibliography']:
        char_score += 1.5  # Common academic section headers
    
    # Penalty for paragraph-like content
    if ('.' in text and text.count('.') > 2) or text.count(',') > 3:
        char_score -= 2  # Strong penalty for sentence-like content
    
    # Question headers (often H2/H3)
    question_words = ['what', 'why', 'how', 'when', 'where', 'which', 'who', 'can', 'will', 'should']
    if any(text_lower.startswith(word) for word in question_words):
        char_score += 0.5
    
    # Factor 4: Position and context
    position_score = 0
    if page_num == 1:  # First page headers are often more important
        position_score += 0.5
    
    # Factor 5: Type-based hints from HURIDOCS
    type_score = 0
    if segment_type == "Title":
        type_score += 2  # Strong indicator for H1
    elif segment_type == "Section header":
        type_score += 1  # Moderate indicator
    
    # Combine all factors
    total_score = size_score + bold_score + char_score + position_score + type_score
    
    # Enhanced classification logic with content pattern consideration
    # Use the content hint to guide final classification
    if content_level_hint == 1 and total_score >= 4.0:  # Strong evidence for H1
        return "H1"
    elif content_level_hint == 2 and total_score >= 3.0:  # Strong evidence for H2
        return "H2"
    elif content_level_hint == 3 and total_score >= 2.0:  # Strong evidence for H3
        return "H3"
    elif total_score >= 5.0:  # Very high threshold for H1
        return "H1"
    elif total_score >= 3.5:  # Higher threshold for H2
        return "H2" 
    elif total_score >= 2.0:  # Moderate threshold for H3
        return "H3"
    else:
        # If score is too low, this is likely body text, not a header
        return None  # Will be filtered out

# --- Function to Organize Document Outline (Revised Logic) ---
def organize_document_outline(huridocs_segments: list) -> dict:
    """
    Processes HURIDOCS segments to extract the main title and classify section headers 
    into H1, H2, H3 based on font size.
    """
    document_title = "Untitled Document"
    outline_items = []

    # Sort segments by page number and then top-left corner for robust reading order
    huridocs_segments.sort(key=lambda s: (s['page_number'], s['top'], s['left']))

    # Analyze font sizes to establish thresholds
    font_thresholds = analyze_font_sizes(huridocs_segments)
    print(f"Font size thresholds: {font_thresholds}")

    all_headers = []
    
    # --- First Pass: Collect all potential headers with enhanced criteria ---
    min_header_size = font_thresholds.get('min_header_size', 11)
    
    for i, segment in enumerate(huridocs_segments):
        text = segment.get("text", "").strip()
        height = segment.get("height", 0)
        font_name = segment.get("font_name", "")
        segment_type = segment.get("type", "")
        
        if not text or height <= 0:
            continue

        # Enhanced header detection criteria - be more inclusive but still selective
        is_potential_header = False
        text_length = len(text)
        avg_body_length = font_thresholds.get('avg_body_length', 50)
        
        # Exclude very long texts (likely paragraphs)
        if text_length > avg_body_length * 1.5:  # Skip texts that are too long to be headers
            continue
            
        # Primary criteria: Type-based detection (most reliable)
        if segment_type in ["Title", "Section header"]:
            is_potential_header = True
        
        # Secondary criteria: Content pattern detection for obvious headers
        text_lower = text.lower()
        if (re.match(r'^(chapter|section|part)\s+\d+', text_lower) or 
            re.match(r'^\d+\.?\s+[A-Z]', text) or  # "1. Introduction", "2.1. Method"
            re.match(r'^\d+\.\d+\.?\s', text) or   # "2.1. ", "3.2.1 "
            re.match(r'^[A-Z][A-Z\s]+$', text) or  # ALL CAPS headers
            text_lower in ['abstract', 'introduction', 'method', 'methods', 'results', 'discussion', 'conclusion', 'conclusions', 'references', 'bibliography', 'overview', 'background', 'applications', 'challenges', 'history']):
            is_potential_header = True
        
        # Tertiary criteria: Short text with larger font (more inclusive)
        if (height >= font_thresholds.get('body_text_size', 10) * 1.1 and  # Slightly larger font
            text_length <= avg_body_length * 0.6):  # Reasonably short text
            is_potential_header = True
        
        # Quaternary criteria: Bold formatting with short text
        font_name_lower = font_name.lower() if font_name else ""
        is_bold = any(indicator in font_name_lower for indicator in ['bold', 'heavy', 'black', 'semibold'])
        
        if (is_bold and text_length <= avg_body_length * 0.5):  # Bold and short
            is_potential_header = True
        
        # Additional check: Question format headers
        if (text.endswith('?') and text_length <= avg_body_length * 0.4):
            is_potential_header = True
        
        # Additional check: Title case short phrases (common header pattern)
        words = text.split()
        if (len(words) <= 5 and  # Short phrase
            all(word[0].isupper() or word.lower() in ['of', 'the', 'and', 'to', 'in', 'a', 'an'] for word in words if word) and  # Title case
            text_length <= avg_body_length * 0.4):  # Short
            is_potential_header = True

        if is_potential_header:
            all_headers.append({
                "text": text,
                "page": segment["page_number"],
                "height": height,
                "font_name": font_name,
                "type": segment_type,
                "index": i
            })

    print(f"Found {len(all_headers)} potential headers")

    # --- Identify the main title and separate it from other headers ---
    title_header = None
    
    # Look for an explicit "Title" type first
    for header in all_headers:
        if header["type"] == "Title":
            title_header = header
            break
    
    # If no explicit title, use the first header on page 1 as the title
    if not title_header:
        page_1_headers = [h for h in all_headers if h["page"] == 1]
        if page_1_headers:
            # Simply take the first header on page 1 as the title
            title_header = page_1_headers[0]
    
    # If still no title found, use the very first header in the document
    if not title_header and all_headers:
        title_header = all_headers[0]

    # Set the document title and remove it from the list of headers to be processed
    if title_header:
        document_title = title_header["text"]
        all_headers = [h for h in all_headers if h["index"] != title_header["index"]]
    else:
        # Fallback: if no headers found at all, keep "Untitled Document"
        document_title = "Untitled Document"

    # --- Second Pass: Classify all remaining headers with multi-factor analysis ---
    for header in all_headers:
        level = classify_header_level(
            text=header["text"],
            font_height=header["height"],
            font_name=header.get("font_name", ""),
            segment_type=header.get("type", ""),
            thresholds=font_thresholds,
            page_num=header["page"]
        )
        
        # Only add items that are classified as actual headers (not None)
        if level is not None:
            outline_items.append({
                "level": level,
                "text": header["text"],
                "page": header["page"]
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