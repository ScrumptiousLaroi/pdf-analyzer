#!/usr/bin/env python3
"""
Script to generate test PDFs with known hierarchical structure for accuracy testing.
Each PDF will have a clear title, H1, H2, H3 headers and body text.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os
import json

def create_test_pdf_1():
    """Create Test PDF 1: Machine Learning Fundamentals"""
    filename = "test_pdfs/test_document_1.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    # Define custom styles
    styles = getSampleStyleSheet()
    
    # Title style (largest)
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # H1 style
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    # H2 style
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )
    
    # H3 style
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=10,
        fontName='Helvetica'
    )
    
    # Content
    story.append(Paragraph("Machine Learning Fundamentals", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("1. Introduction to Machine Learning", h1_style))
    story.append(Paragraph("Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every task.", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1.1 What is Machine Learning?", h2_style))
    story.append(Paragraph("Machine learning algorithms build mathematical models based on training data to make predictions or decisions.", body_style))
    
    story.append(Paragraph("1.1.1 Types of Learning", h3_style))
    story.append(Paragraph("There are three main types of machine learning: supervised, unsupervised, and reinforcement learning.", body_style))
    
    story.append(Paragraph("1.1.2 Applications", h3_style))
    story.append(Paragraph("Machine learning is used in various applications including image recognition, natural language processing, and recommendation systems.", body_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("2. Supervised Learning", h1_style))
    story.append(Paragraph("Supervised learning uses labeled training data to learn a mapping from inputs to outputs.", body_style))
    
    story.append(Paragraph("2.1 Classification", h2_style))
    story.append(Paragraph("Classification algorithms predict discrete class labels for input data.", body_style))
    
    story.append(Paragraph("2.1.1 Decision Trees", h3_style))
    story.append(Paragraph("Decision trees create a model that predicts target values by learning simple decision rules inferred from data features.", body_style))
    
    story.append(Paragraph("2.2 Regression", h2_style))
    story.append(Paragraph("Regression algorithms predict continuous numerical values rather than discrete classes.", body_style))
    
    doc.build(story)
    return filename

def create_test_pdf_2():
    """Create Test PDF 2: Data Science Methods"""
    filename = "test_pdfs/test_document_2.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=18, spaceAfter=25, alignment=TA_CENTER, fontName='Helvetica-Bold')
    h1_style = ParagraphStyle('CustomH1', parent=styles['Heading1'], fontSize=15, spaceAfter=18, fontName='Helvetica-Bold')
    h2_style = ParagraphStyle('CustomH2', parent=styles['Heading2'], fontSize=13, spaceAfter=15, fontName='Helvetica-Bold')
    h3_style = ParagraphStyle('CustomH3', parent=styles['Heading3'], fontSize=11, spaceAfter=12, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=10, spaceAfter=10, fontName='Helvetica')
    
    # Content
    story.append(Paragraph("Data Science Methods and Techniques", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Abstract", h1_style))
    story.append(Paragraph("This document covers fundamental data science methods including data collection, analysis, and visualization techniques used in modern research.", body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Introduction", h1_style))
    story.append(Paragraph("Data science combines statistical analysis, machine learning, and domain expertise to extract insights from structured and unstructured data.", body_style))
    
    story.append(Paragraph("Data Collection Methods", h2_style))
    story.append(Paragraph("Effective data collection is crucial for any data science project.", body_style))
    
    story.append(Paragraph("Survey Design", h3_style))
    story.append(Paragraph("Surveys must be carefully designed to avoid bias and ensure representative sampling of the target population.", body_style))
    
    story.append(Paragraph("Web Scraping", h3_style))
    story.append(Paragraph("Automated data collection from websites requires understanding of HTML structure and ethical considerations.", body_style))
    
    story.append(Paragraph("Data Analysis Techniques", h2_style))
    story.append(Paragraph("Various statistical and computational methods can be applied to analyze collected data.", body_style))
    
    story.append(Paragraph("Exploratory Data Analysis", h3_style))
    story.append(Paragraph("EDA involves summarizing main characteristics of data through visual and statistical methods.", body_style))
    
    story.append(Paragraph("Results and Discussion", h1_style))
    story.append(Paragraph("The application of these methods demonstrates their effectiveness in extracting meaningful insights from complex datasets.", body_style))
    
    doc.build(story)
    return filename

def create_test_pdf_3():
    """Create Test PDF 3: Software Engineering Principles"""
    filename = "test_pdfs/test_document_3.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=22, spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    h1_style = ParagraphStyle('CustomH1', parent=styles['Heading1'], fontSize=17, spaceAfter=20, fontName='Helvetica-Bold')
    h2_style = ParagraphStyle('CustomH2', parent=styles['Heading2'], fontSize=14, spaceAfter=15, fontName='Helvetica-Bold')
    h3_style = ParagraphStyle('CustomH3', parent=styles['Heading3'], fontSize=12, spaceAfter=12, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=10, spaceAfter=10, fontName='Helvetica')
    
    # Content with numbered sections
    story.append(Paragraph("Software Engineering Principles", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Chapter 1: Development Methodologies", h1_style))
    story.append(Paragraph("Software development methodologies provide structured approaches to building software systems efficiently and effectively.", body_style))
    
    story.append(Paragraph("1.1 Agile Development", h2_style))
    story.append(Paragraph("Agile methodology emphasizes iterative development, collaboration, and flexibility in response to changing requirements.", body_style))
    
    story.append(Paragraph("1.1.1 Scrum Framework", h3_style))
    story.append(Paragraph("Scrum is an agile framework that organizes work into time-boxed iterations called sprints.", body_style))
    
    story.append(Paragraph("1.1.2 Kanban Method", h3_style))
    story.append(Paragraph("Kanban visualizes workflow and limits work in progress to improve efficiency and identify bottlenecks.", body_style))
    
    story.append(Paragraph("1.2 Waterfall Model", h2_style))
    story.append(Paragraph("The waterfall model follows a linear sequential approach where each phase must be completed before the next begins.", body_style))
    
    story.append(Paragraph("Chapter 2: Code Quality and Testing", h1_style))
    story.append(Paragraph("Maintaining high code quality through testing and best practices is essential for sustainable software development.", body_style))
    
    story.append(Paragraph("2.1 Unit Testing", h2_style))
    story.append(Paragraph("Unit tests verify that individual components of the software work correctly in isolation.", body_style))
    
    story.append(Paragraph("2.1.1 Test-Driven Development", h3_style))
    story.append(Paragraph("TDD involves writing tests before implementing functionality, ensuring code meets requirements from the start.", body_style))
    
    story.append(Paragraph("2.2 Integration Testing", h2_style))
    story.append(Paragraph("Integration tests verify that different components work correctly when combined together.", body_style))
    
    doc.build(story)
    return filename

def create_test_pdf_4():
    """Create Test PDF 4: Research Paper Format"""
    filename = "test_pdfs/test_document_4.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Different font sizes to test edge cases
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=19, spaceAfter=25, alignment=TA_CENTER, fontName='Helvetica-Bold')
    h1_style = ParagraphStyle('CustomH1', parent=styles['Heading1'], fontSize=14, spaceAfter=18, fontName='Helvetica-Bold')
    h2_style = ParagraphStyle('CustomH2', parent=styles['Heading2'], fontSize=12, spaceAfter=15, fontName='Helvetica-Bold')
    h3_style = ParagraphStyle('CustomH3', parent=styles['Heading3'], fontSize=11, spaceAfter=12, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=10, spaceAfter=10, fontName='Helvetica')
    
    # Research paper content
    story.append(Paragraph("Impact of Artificial Intelligence on Modern Healthcare", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Abstract", h1_style))
    story.append(Paragraph("This study examines the transformative effects of artificial intelligence technologies on healthcare delivery, patient outcomes, and medical research methodologies.", body_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph("Artificial intelligence has emerged as a revolutionary force in healthcare, offering unprecedented opportunities for improving diagnosis, treatment, and patient care.", body_style))
    
    story.append(Paragraph("1.1 Background and Motivation", h2_style))
    story.append(Paragraph("The healthcare industry faces numerous challenges including rising costs, aging populations, and the need for more personalized treatment approaches.", body_style))
    
    story.append(Paragraph("1.1.1 Current Healthcare Challenges", h3_style))
    story.append(Paragraph("Healthcare systems worldwide struggle with resource allocation, diagnostic accuracy, and treatment optimization in an increasingly complex medical landscape.", body_style))
    
    story.append(Paragraph("1.2 Research Objectives", h2_style))
    story.append(Paragraph("This research aims to analyze the current state of AI implementation in healthcare and identify key areas for future development.", body_style))
    
    story.append(Paragraph("2. Literature Review", h1_style))
    story.append(Paragraph("Previous studies have shown significant potential for AI applications in medical imaging, drug discovery, and clinical decision support systems.", body_style))
    
    story.append(Paragraph("2.1 AI in Medical Imaging", h2_style))
    story.append(Paragraph("Machine learning algorithms have demonstrated remarkable accuracy in interpreting medical images, often surpassing human radiologists in specific tasks.", body_style))
    
    story.append(Paragraph("2.1.1 Deep Learning Applications", h3_style))
    story.append(Paragraph("Convolutional neural networks have proven particularly effective for analyzing X-rays, MRIs, and CT scans with high precision.", body_style))
    
    story.append(Paragraph("3. Methodology", h1_style))
    story.append(Paragraph("Our research methodology combines quantitative analysis of AI implementation data with qualitative interviews of healthcare professionals.", body_style))
    
    story.append(Paragraph("Conclusion", h1_style))
    story.append(Paragraph("AI technologies represent a paradigm shift in healthcare delivery with the potential to significantly improve patient outcomes and operational efficiency.", body_style))
    
    doc.build(story)
    return filename

def create_test_pdf_5():
    """Create Test PDF 5: Technical Manual Format"""
    filename = "test_pdfs/test_document_5.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Technical manual styling with different font patterns
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=24, spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    h1_style = ParagraphStyle('CustomH1', parent=styles['Heading1'], fontSize=18, spaceAfter=20, fontName='Helvetica-Bold')
    h2_style = ParagraphStyle('CustomH2', parent=styles['Heading2'], fontSize=15, spaceAfter=15, fontName='Helvetica-Bold')
    h3_style = ParagraphStyle('CustomH3', parent=styles['Heading3'], fontSize=13, spaceAfter=12, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=11, spaceAfter=10, fontName='Helvetica')
    
    # Technical manual content
    story.append(Paragraph("API Integration Guide", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Getting Started", h1_style))
    story.append(Paragraph("This guide provides comprehensive instructions for integrating with our REST API, including authentication, endpoint usage, and best practices.", body_style))
    
    story.append(Paragraph("Prerequisites", h2_style))
    story.append(Paragraph("Before beginning the integration process, ensure you have the necessary development environment and API credentials.", body_style))
    
    story.append(Paragraph("System Requirements", h3_style))
    story.append(Paragraph("Your system must support HTTPS connections and JSON data parsing. Minimum requirements include Python 3.7 or Node.js 14.0.", body_style))
    
    story.append(Paragraph("Installation Steps", h3_style))
    story.append(Paragraph("Follow these steps to install the required dependencies and configure your development environment for API integration.", body_style))
    
    story.append(Paragraph("Authentication", h2_style))
    story.append(Paragraph("Our API uses OAuth 2.0 for secure authentication. All requests must include a valid access token in the authorization header.", body_style))
    
    story.append(Paragraph("API Endpoints", h1_style))
    story.append(Paragraph("The following sections describe all available API endpoints, their parameters, and expected responses.", body_style))
    
    story.append(Paragraph("User Management", h2_style))
    story.append(Paragraph("User management endpoints allow you to create, update, retrieve, and delete user accounts through programmatic access.", body_style))
    
    story.append(Paragraph("Creating Users", h3_style))
    story.append(Paragraph("To create a new user account, send a POST request to the /users endpoint with the required user information in JSON format.", body_style))
    
    story.append(Paragraph("Updating User Information", h3_style))
    story.append(Paragraph("User information can be updated using PATCH requests to the /users/{id} endpoint with the fields you want to modify.", body_style))
    
    story.append(Paragraph("Data Operations", h2_style))
    story.append(Paragraph("Data operation endpoints provide CRUD functionality for managing application data through RESTful interfaces.", body_style))
    
    story.append(Paragraph("Error Handling", h1_style))
    story.append(Paragraph("Proper error handling is essential for robust API integration. Our API returns standard HTTP status codes with descriptive error messages.", body_style))
    
    doc.build(story)
    return filename

def create_test_pdf_6():
    """Create Test PDF 6: Report Format with Mixed Patterns"""
    filename = "test_pdfs/test_document_6.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Report styling with closer font sizes (challenging case)
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=16, spaceAfter=25, alignment=TA_CENTER, fontName='Helvetica-Bold')
    h1_style = ParagraphStyle('CustomH1', parent=styles['Heading1'], fontSize=14, spaceAfter=18, fontName='Helvetica-Bold')
    h2_style = ParagraphStyle('CustomH2', parent=styles['Heading2'], fontSize=13, spaceAfter=15, fontName='Helvetica-Bold')
    h3_style = ParagraphStyle('CustomH3', parent=styles['Heading3'], fontSize=12, spaceAfter=12, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=11, spaceAfter=10, fontName='Helvetica')
    
    # Report content with mixed formatting patterns
    story.append(Paragraph("Q4 2024 Performance Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph("This quarterly report presents a comprehensive analysis of company performance metrics, financial indicators, and strategic initiatives implemented during Q4 2024.", body_style))
    
    story.append(Paragraph("Financial Performance", h1_style))
    story.append(Paragraph("The financial analysis reveals significant growth across multiple revenue streams with particular strength in digital transformation initiatives.", body_style))
    
    story.append(Paragraph("Revenue Analysis", h2_style))
    story.append(Paragraph("Total revenue for Q4 2024 reached $2.3M, representing a 15% increase compared to the previous quarter and exceeding projected targets.", body_style))
    
    story.append(Paragraph("Product Sales", h3_style))
    story.append(Paragraph("Core product sales contributed 65% of total revenue, with new product launches accounting for an additional 12% revenue growth.", body_style))
    
    story.append(Paragraph("Service Revenue", h3_style))
    story.append(Paragraph("Professional services and consulting revenue grew by 23%, indicating strong market demand for our expertise and solutions.", body_style))
    
    story.append(Paragraph("Cost Management", h2_style))
    story.append(Paragraph("Operational costs were effectively controlled through strategic automation initiatives and process optimization programs.", body_style))
    
    story.append(Paragraph("Operational Metrics", h1_style))
    story.append(Paragraph("Key operational indicators demonstrate improved efficiency and customer satisfaction across all business units.", body_style))
    
    story.append(Paragraph("Customer Satisfaction", h2_style))
    story.append(Paragraph("Customer satisfaction scores reached an all-time high of 4.8/5.0, reflecting our commitment to service excellence and quality delivery.", body_style))
    
    story.append(Paragraph("Response Time Improvements", h3_style))
    story.append(Paragraph("Average customer support response time decreased by 40% through implementation of AI-powered ticketing systems and process improvements.", body_style))
    
    story.append(Paragraph("What's Next for 2025?", h1_style))
    story.append(Paragraph("Looking ahead to 2025, our strategic focus will center on expanding market presence, enhancing product capabilities, and strengthening customer relationships.", body_style))
    
    story.append(Paragraph("Strategic Initiatives", h2_style))
    story.append(Paragraph("Key initiatives for the upcoming year include international expansion, technology infrastructure upgrades, and talent acquisition in critical areas.", body_style))
    
    doc.build(story)
    return filename

def create_expected_outputs():
    """Create expected JSON outputs for each test PDF"""
    
    # Expected output for test_document_1.pdf
    expected_1 = {
        "title": "Machine Learning Fundamentals",
        "outline": [
            {"level": "H1", "text": "1. Introduction to Machine Learning", "page": 1},
            {"level": "H2", "text": "1.1 What is Machine Learning?", "page": 1},
            {"level": "H3", "text": "1.1.1 Types of Learning", "page": 1},
            {"level": "H3", "text": "1.1.2 Applications", "page": 1},
            {"level": "H1", "text": "2. Supervised Learning", "page": 1},
            {"level": "H2", "text": "2.1 Classification", "page": 1},
            {"level": "H3", "text": "2.1.1 Decision Trees", "page": 1},
            {"level": "H2", "text": "2.2 Regression", "page": 1}
        ]
    }
    
    # Expected output for test_document_2.pdf
    # Based on font sizes: Title=17, H1=14, H2=12, H3=10
    expected_2 = {
        "title": "Data Science Methods and Techniques",
        "outline": [
            {"level": "H1", "text": "Abstract", "page": 1},
            {"level": "H1", "text": "Introduction", "page": 1},
            {"level": "H2", "text": "Data Collection Methods", "page": 1},
            {"level": "H2", "text": "Survey Design", "page": 1},  # These are H2 based on font size
            {"level": "H2", "text": "Web Scraping", "page": 1},   # These are H2 based on font size
            {"level": "H2", "text": "Data Analysis Techniques", "page": 1},
            {"level": "H2", "text": "Exploratory Data Analysis", "page": 1},  # These are H2 based on font size
            {"level": "H1", "text": "Results and Discussion", "page": 1}
        ]
    }
    
    # Expected output for test_document_3.pdf
    expected_3 = {
        "title": "Software Engineering Principles",
        "outline": [
            {"level": "H1", "text": "Chapter 1: Development Methodologies", "page": 1},
            {"level": "H2", "text": "1.1 Agile Development", "page": 1},
            {"level": "H3", "text": "1.1.1 Scrum Framework", "page": 1},
            {"level": "H3", "text": "1.1.2 Kanban Method", "page": 1},
            {"level": "H2", "text": "1.2 Waterfall Model", "page": 1},
            {"level": "H1", "text": "Chapter 2: Code Quality and Testing", "page": 1},
            {"level": "H2", "text": "2.1 Unit Testing", "page": 1},
            {"level": "H3", "text": "2.1.1 Test-Driven Development", "page": 1},
            {"level": "H2", "text": "2.2 Integration Testing", "page": 1}
        ]
    }
    
    # Expected output for test_document_4.pdf (Research Paper)
    expected_4 = {
        "title": "Impact of Artificial Intelligence on Modern Healthcare",
        "outline": [
            {"level": "H1", "text": "Abstract", "page": 1},
            {"level": "H1", "text": "1. Introduction", "page": 1},
            {"level": "H2", "text": "1.1 Background and Motivation", "page": 1},
            {"level": "H3", "text": "1.1.1 Current Healthcare Challenges", "page": 1},
            {"level": "H2", "text": "1.2 Research Objectives", "page": 1},
            {"level": "H1", "text": "2. Literature Review", "page": 1},
            {"level": "H2", "text": "2.1 AI in Medical Imaging", "page": 1},
            {"level": "H3", "text": "2.1.1 Deep Learning Applications", "page": 1},
            {"level": "H1", "text": "3. Methodology", "page": 1},
            {"level": "H1", "text": "Conclusion", "page": 1}
        ]
    }
    
    # Expected output for test_document_5.pdf (Technical Manual)
    expected_5 = {
        "title": "API Integration Guide",
        "outline": [
            {"level": "H1", "text": "Getting Started", "page": 1},
            {"level": "H2", "text": "Prerequisites", "page": 1},
            {"level": "H3", "text": "System Requirements", "page": 1},
            {"level": "H3", "text": "Installation Steps", "page": 1},
            {"level": "H2", "text": "Authentication", "page": 1},
            {"level": "H1", "text": "API Endpoints", "page": 1},
            {"level": "H2", "text": "User Management", "page": 1},
            {"level": "H3", "text": "Creating Users", "page": 1},
            {"level": "H3", "text": "Updating User Information", "page": 1},
            {"level": "H2", "text": "Data Operations", "page": 1},
            {"level": "H1", "text": "Error Handling", "page": 1}
        ]
    }
    
    # Expected output for test_document_6.pdf (Report with close font sizes)
    expected_6 = {
        "title": "Q4 2024 Performance Analysis Report",
        "outline": [
            {"level": "H1", "text": "Executive Summary", "page": 1},
            {"level": "H1", "text": "Financial Performance", "page": 1},
            {"level": "H2", "text": "Revenue Analysis", "page": 1},
            {"level": "H3", "text": "Product Sales", "page": 1},
            {"level": "H3", "text": "Service Revenue", "page": 1},
            {"level": "H2", "text": "Cost Management", "page": 1},
            {"level": "H1", "text": "Operational Metrics", "page": 1},
            {"level": "H2", "text": "Customer Satisfaction", "page": 1},
            {"level": "H3", "text": "Response Time Improvements", "page": 1},
            {"level": "H1", "text": "What's Next for 2025?", "page": 1},
            {"level": "H2", "text": "Strategic Initiatives", "page": 1}
        ]
    }
    
    # Save all expected outputs
    with open("expected_output/test_document_1_outline.json", 'w', encoding='utf-8') as f:
        json.dump(expected_1, f, indent=4, ensure_ascii=False)
    
    with open("expected_output/test_document_2_outline.json", 'w', encoding='utf-8') as f:
        json.dump(expected_2, f, indent=4, ensure_ascii=False)
    
    with open("expected_output/test_document_3_outline.json", 'w', encoding='utf-8') as f:
        json.dump(expected_3, f, indent=4, ensure_ascii=False)
    
    with open("expected_output/test_document_4_outline.json", 'w', encoding='utf-8') as f:
        json.dump(expected_4, f, indent=4, ensure_ascii=False)
    
    with open("expected_output/test_document_5_outline.json", 'w', encoding='utf-8') as f:
        json.dump(expected_5, f, indent=4, ensure_ascii=False)
    
    with open("expected_output/test_document_6_outline.json", 'w', encoding='utf-8') as f:
        json.dump(expected_6, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("test_pdfs", exist_ok=True)
    os.makedirs("expected_output", exist_ok=True)
    
    print("Generating test PDFs...")
    
    pdf1 = create_test_pdf_1()
    print(f"Created: {pdf1}")
    
    pdf2 = create_test_pdf_2()
    print(f"Created: {pdf2}")
    
    pdf3 = create_test_pdf_3()
    print(f"Created: {pdf3}")
    
    pdf4 = create_test_pdf_4()
    print(f"Created: {pdf4}")
    
    pdf5 = create_test_pdf_5()
    print(f"Created: {pdf5}")
    
    pdf6 = create_test_pdf_6()
    print(f"Created: {pdf6}")
    
    print("\nGenerating expected JSON outputs...")
    create_expected_outputs()
    print("Created expected output files in 'expected_output/' folder")
    
    print("\nTest PDF generation complete!")
    print("Files created:")
    print("- test_pdfs/test_document_1.pdf")
    print("- test_pdfs/test_document_2.pdf")
    print("- test_pdfs/test_document_3.pdf")
    print("- test_pdfs/test_document_4.pdf")
    print("- test_pdfs/test_document_5.pdf")
    print("- test_pdfs/test_document_6.pdf")
    print("- expected_output/test_document_1_outline.json")
    print("- expected_output/test_document_2_outline.json")
    print("- expected_output/test_document_3_outline.json")
    print("- expected_output/test_document_4_outline.json")
    print("- expected_output/test_document_5_outline.json")
    print("- expected_output/test_document_6_outline.json")
