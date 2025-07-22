# PDF Document Outline Extraction - Accuracy Testing Framework

This framework provides comprehensive testing and accuracy measurement for the PDF document outline extraction system. It generates test PDFs with known hierarchical structure, processes them through the extraction pipeline, and calculates detailed accuracy metrics.

## Extending the Framework

### Quick Command Reference

```bash
# Generate 6 test PDFs only
python generate_test_pdfs.py

# Run full accuracy test (generates PDFs + tests)
python test_accuracy.py --generate

# Test existing PDFs without regenerating
python test_accuracy.py --test-only

# Process your own PDFs
python pdf_processor.py

# Check what files were created
ls test_pdfs/        # 6 test PDF files
ls expected_output/  # 6 expected JSON files  
ls output/          # Generated JSON results
```

The testing framework consists of three main components:

1. **Test PDF Generator** (`generate_test_pdfs.py`) - Creates PDFs with known hierarchical structure
2. **Accuracy Tester** (`test_accuracy.py`) - Runs tests and calculates accuracy metrics
3. **Expected Outputs** (`expected_output/`) - Reference JSON files for comparison

## Quick Start

### Option 1: Generate Test PDFs and Run Full Accuracy Test
```bash
# Install required dependencies
pip install reportlab

# Generate all 6 test PDFs and run comprehensive accuracy test
python test_accuracy.py --generate
```

### Option 2: Run Test Only (if test PDFs already exist)
```bash
# Run tests on existing test PDFs without regenerating them
python test_accuracy.py --test-only
```

### Option 3: Generate Test PDFs Only
```bash
# Just generate the 6 test PDF files without running tests
python generate_test_pdfs.py
```

### Option 4: Test with Your Own PDF Files
```bash
# Step 1: Place your PDF files in the input/ folder
cp your_document.pdf input/

# Step 2: Run the PDF processor on your files
python pdf_processor.py

# Step 3: Check results in the output/ folder
ls output/
cat output/your_document_outline.json
```

## Test Documents

The framework generates **six test documents** with different characteristics to thoroughly test the system:

### 1. Machine Learning Fundamentals (test_document_1.pdf)
- **Font Hierarchy**: Title (20pt) → H1 (16pt) → H2 (14pt) → H3 (12pt)
- **Structure**: Numbered sections with clear hierarchy (1., 1.1, 1.1.1)
- **Content**: Technical document with nested subsections
- **Expected Accuracy**: High (numbered patterns help classification)

### 2. Data Science Methods and Techniques (test_document_2.pdf)  
- **Font Hierarchy**: Title (18pt) → H1 (15pt) → H2 (13pt) → H3 (11pt)
- **Structure**: Academic paper format (Abstract, Introduction, etc.)
- **Content**: Mixed hierarchy with both numbered and unnumbered sections
- **Expected Accuracy**: Medium (some ambiguous hierarchical relationships)

### 3. Software Engineering Principles (test_document_3.pdf)
- **Font Hierarchy**: Title (22pt) → H1 (17pt) → H2 (14pt) → H3 (12pt)
- **Structure**: Chapter-based with clear numbered hierarchy
- **Content**: Textbook-style with "Chapter X:" prefixes
- **Expected Accuracy**: High (strong hierarchical patterns)

### 4. Impact of AI on Modern Healthcare (test_document_4.pdf)
- **Font Hierarchy**: Title (19pt) → H1 (14pt) → H2 (12pt) → H3 (11pt)
- **Structure**: Research paper with numbered sections and conclusion
- **Content**: Academic research format with literature review
- **Expected Accuracy**: High (clear numbered hierarchy with research patterns)

### 5. API Integration Guide (test_document_5.pdf)
- **Font Hierarchy**: Title (24pt) → H1 (18pt) → H2 (15pt) → H3 (13pt)
- **Structure**: Technical manual with procedural sections
- **Content**: Documentation-style with getting started guides
- **Expected Accuracy**: Medium (technical documentation patterns)

### 6. Q4 2024 Performance Analysis Report (test_document_6.pdf)
- **Font Hierarchy**: Title (16pt) → H1 (14pt) → H2 (13pt) → H3 (12pt)
- **Structure**: Business report with close font sizes (challenging case)
- **Content**: Executive summary, metrics, and strategic planning
- **Expected Accuracy**: Low-Medium (close font sizes test classification limits)

## Accuracy Metrics

The testing framework calculates multiple accuracy metrics:

### Title Accuracy
- **Metric**: Percentage of documents with correctly extracted titles
- **Target**: 100% (title extraction should be highly reliable)

### Outline Accuracy
- **Precision**: Correct extractions / Total extractions
- **Recall**: Correct extractions / Total expected items
- **F1 Score**: Harmonic mean of precision and recall
- **Exact Match Rate**: Percentage of perfectly matched outline items

### Performance Grades
- **Excellent** (90-100%): Production-ready performance
- **Good** (80-89%): Acceptable with minor improvements needed
- **Fair** (70-79%): Needs optimization before production use
- **Needs Improvement** (60-69%): Significant issues to address
- **Poor** (<60%): Major algorithmic changes required

## Current Performance

**Latest Test Results (6 Documents):**
- **Title Accuracy**: 100% ✅
- **Average F1 Score**: 70.3% 👌
- **Overall Performance**: Fair (down from previous 3-document test due to challenging cases)

**Individual Document Results:**
- **test_document_1.pdf**: 100% accuracy (8/8 exact matches) ✅
- **test_document_2.pdf**: 87.5% accuracy (7/8 exact matches) ✅  
- **test_document_3.pdf**: 100% accuracy (9/9 exact matches) ✅
- **test_document_4.pdf**: 80.0% accuracy (8/10 exact matches) 👍
- **test_document_5.pdf**: 27.3% accuracy (3/11 exact matches) ⚠️
- **test_document_6.pdf**: 27.3% accuracy (3/11 exact matches) ⚠️

**Performance Analysis:**
- Documents 1-3: Excellent performance (original test set)
- Document 4: Good performance (research paper format)  
- Documents 5-6: Challenging cases revealing system limitations with close font sizes

### Test Document Characteristics Summary

| Document | Type | Font Range | Hierarchy Pattern | Difficulty | Accuracy |
|----------|------|------------|-------------------|------------|----------|
| 1 | Technical | 12-20pt | Numbered (1.1.1) | Easy | 100% ✅ |
| 2 | Academic | 11-18pt | Mixed patterns | Medium | 87.5% ✅ |
| 3 | Textbook | 12-22pt | Chapter-based | Easy | 100% ✅ |
| 4 | Research | 11-19pt | Research format | Medium | 80.0% 👍 |
| 5 | Technical Manual | 13-24pt | Procedural | Hard | 27.3% ⚠️ |
| 6 | Business Report | 12-16pt | Close font sizes | Hard | 27.3% ⚠️ |

**Key Insights:**
- **Numbered hierarchies** (1., 1.1, 1.1.1) achieve highest accuracy
- **Font size differences** of 2+ points work well
- **Close font sizes** (<2pt difference) challenge the algorithm
- **Content patterns** help significantly in classification

## File Structure

```
pdf_analyzer_huridocs/
├── test_pdfs/                    # Generated test PDF files (6 documents)
│   ├── test_document_1.pdf       # Machine Learning (numbered hierarchy)
│   ├── test_document_2.pdf       # Data Science (academic format)
│   ├── test_document_3.pdf       # Software Engineering (chapter-based)
│   ├── test_document_4.pdf       # AI Healthcare (research paper)
│   ├── test_document_5.pdf       # API Guide (technical manual)
│   └── test_document_6.pdf       # Performance Report (close font sizes)
├── expected_output/              # Reference JSON outputs (6 files)
│   ├── test_document_1_outline.json
│   ├── test_document_2_outline.json
│   ├── test_document_3_outline.json
│   ├── test_document_4_outline.json
│   ├── test_document_5_outline.json
│   └── test_document_6_outline.json
├── output/                       # Actual processing results
│   ├── test_document_1_outline.json
│   ├── test_document_2_outline.json
│   ├── test_document_3_outline.json
│   ├── test_document_4_outline.json
│   ├── test_document_5_outline.json
│   └── test_document_6_outline.json
├── input/                        # Place your own PDF files here
├── generate_test_pdfs.py         # Generates 6 test PDF documents
├── test_accuracy.py              # Accuracy testing framework
├── pdf_processor.py              # Main processing logic
└── accuracy_test_results.json    # Detailed test results
```

## Algorithm Features Tested

### Font Size Analysis
- Dynamic threshold calculation based on document content
- Body text size identification using statistical analysis
- Multi-level header classification (H1, H2, H3)

### Content Pattern Recognition
- Numbered section detection (1., 1.1, 1.1.1)
- Academic format recognition (Abstract, Introduction, etc.)
- Chapter-based pattern matching

### Multi-Factor Classification
- Font size scoring (primary factor)
- Content pattern hints (secondary factor)
- Bold formatting detection
- Text length analysis
- Position and context consideration

## Testing with Your Own PDF Files

### Step-by-Step Guide

1. **Prepare Your PDF Files**
   ```bash
   # Create the input directory if it doesn't exist
   mkdir -p input
   
   # Copy your PDF files to the input folder
   cp /path/to/your/document.pdf input/
   cp /path/to/another/document.pdf input/
   ```

2. **Process Your Documents**
   ```bash
   # Run the PDF processor on all files in input/
   python pdf_processor.py
   ```

3. **Check Results**
   ```bash
   # List generated outline files
   ls output/
   
   # View a specific outline
   cat output/your_document_outline.json
   
   # Pretty print JSON for better readability
   python -m json.tool output/your_document_outline.json
   ```

### Understanding Your Results

Your output JSON will have this structure:
```json
{
    "title": "Your Document Title",
    "outline": [
        {
            "level": "H1",
            "text": "Chapter 1: Introduction",
            "page": 1
        },
        {
            "level": "H2", 
            "text": "1.1 Background",
            "page": 1
        }
    ]
}
```

### Creating Expected Outputs for Your Documents

If you want to test accuracy on your own documents:

1. **Create Expected Output Files**
   ```bash
   # Create expected output directory
   mkdir -p expected_output
   
   # Manually create expected JSON for your document
   cat > expected_output/your_document_outline.json << 'EOF'
   {
       "title": "Expected Title",
       "outline": [
           {"level": "H1", "text": "Expected Section", "page": 1}
       ]
   }
   EOF
   ```

2. **Run Custom Accuracy Test**
   ```bash
   # Move your PDFs to test_pdfs folder temporarily
   cp input/your_document.pdf test_pdfs/
   
   # Run accuracy test
   python test_accuracy.py --test-only
   ```

### Adding New Test Documents

1. **Create PDF Generation Function** in `generate_test_pdfs.py`:
```python
def create_test_pdf_4():
    # Define document structure with known hierarchy
    # Use consistent font sizes for each level
    # Return filename
```

2. **Define Expected Output**:
```python
expected_4 = {
    "title": "Document Title",
    "outline": [
        {"level": "H1", "text": "Section 1", "page": 1},
        {"level": "H2", "text": "Subsection 1.1", "page": 1},
        # ... more outline items
    ]
}
```

3. **Update Test Runner** to include new document in processing loop

### Custom Accuracy Metrics

The `AccuracyTester` class can be extended with additional metrics:

```python
def calculate_custom_metric(self, expected, actual):
    # Implement custom accuracy calculation
    return metric_score
```

## Troubleshooting

### Common Issues

1. **HURIDOCS Service Not Running**
   - Ensure Docker container is running: `docker ps`
   - Start service: `docker-compose up -d`

2. **Font Size Mismatches**
   - Check actual font sizes with debug output
   - Adjust thresholds in classification algorithm
   - Verify PDF generation uses intended font sizes

3. **Low Accuracy Scores**
   - Review individual document results for patterns
   - Check if expected outputs match algorithm logic
   - Consider adjusting classification weights

### Debug Mode

Enable debug output in `pdf_processor.py`:
```python
print(f"Font size thresholds: {font_thresholds}")
print(f"Found {len(all_headers)} potential headers")
```

## Dependencies

- **Python 3.7+**
- **reportlab**: PDF generation
- **requests**: HURIDOCS API communication
- **HURIDOCS Docker Service**: Document layout analysis

## Future Enhancements

1. **Cross-Document Validation**: Test consistency across similar document types
2. **Performance Benchmarking**: Measure processing speed and memory usage
3. **Error Analysis**: Detailed categorization of classification errors
4. **Automated Regression Testing**: CI/CD integration for continuous validation
5. **Multi-Language Support**: Test documents in different languages
6. **Complex Layout Testing**: Tables, figures, multi-column layouts

---

*Framework developed to ensure reliable PDF document outline extraction with measurable accuracy metrics.*
