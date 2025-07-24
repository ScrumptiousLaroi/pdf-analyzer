This directory will contain the structured JSON output files after processing PDFs.

Each processed PDF will generate a corresponding JSON file with:
- Document title
- Hierarchical outline structure (H1, H2, H3, H4)
- Page numbers for each section

Example output format:
{
    "title": "Document Title",
    "outline": [
        {
            "level": "H1",
            "text": "Section Header",
            "page": 1
        }
    ]
}
