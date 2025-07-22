#!/usr/bin/env python3
"""
Accuracy Testing Script for PDF Document Outline Extraction

This script:
1. Runs the PDF processor on test documents
2. Compares actual output with expected output
3. Calculates accuracy metrics for title and hierarchy detection
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Tuple
import argparse

class AccuracyTester:
    def __init__(self, test_pdfs_folder="test_pdfs", expected_folder="expected_output", actual_folder="output"):
        self.test_pdfs_folder = test_pdfs_folder
        self.expected_folder = expected_folder
        self.actual_folder = actual_folder
        self.results = {}
        
    def run_pdf_processor(self) -> bool:
        """Run the PDF processor on test documents"""
        try:
            print("Running PDF processor on test documents...")
            
            # First, copy test PDFs to input folder
            test_files = [f for f in os.listdir(self.test_pdfs_folder) if f.endswith('.pdf')]
            
            if not test_files:
                print(f"No test PDF files found in {self.test_pdfs_folder}")
                return False
            
            # Clear input folder and copy test files
            input_folder = "input"
            os.makedirs(input_folder, exist_ok=True)
            
            # Remove existing files in input folder
            for f in os.listdir(input_folder):
                if f.endswith('.pdf'):
                    os.remove(os.path.join(input_folder, f))
            
            # Copy test files to input folder
            import shutil
            for test_file in test_files:
                src = os.path.join(self.test_pdfs_folder, test_file)
                dst = os.path.join(input_folder, test_file)
                shutil.copy2(src, dst)
                print(f"Copied {test_file} to input folder")
            
            # Run the PDF processor
            result = subprocess.run([sys.executable, "pdf_processor.py"], 
                                  capture_output=True, text=True, cwd=".")
            
            if result.returncode != 0:
                print(f"PDF processor failed with error: {result.stderr}")
                return False
                
            print("PDF processor completed successfully")
            print(f"Output: {result.stdout}")
            return True
            
        except Exception as e:
            print(f"Error running PDF processor: {e}")
            return False
    
    def load_json_file(self, filepath: str) -> Dict:
        """Load and return JSON data from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {filepath}: {e}")
            return None
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison (remove extra spaces, case-insensitive)"""
        return text.strip().lower()
    
    def compare_titles(self, expected: Dict, actual: Dict) -> Tuple[bool, str]:
        """Compare document titles"""
        expected_title = expected.get("title", "").strip()
        actual_title = actual.get("title", "").strip()
        
        if not expected_title and not actual_title:
            return True, "Both titles empty"
        
        # Normalize for comparison
        exp_norm = self.normalize_text(expected_title)
        act_norm = self.normalize_text(actual_title)
        
        match = exp_norm == act_norm
        message = f"Expected: '{expected_title}' | Actual: '{actual_title}'"
        
        return match, message
    
    def compare_outlines(self, expected: Dict, actual: Dict) -> Dict:
        """Compare document outlines and return detailed metrics"""
        expected_outline = expected.get("outline", [])
        actual_outline = actual.get("outline", [])
        
        # Create comparison metrics
        metrics = {
            "total_expected": len(expected_outline),
            "total_actual": len(actual_outline),
            "exact_matches": 0,
            "level_matches": 0,
            "text_matches": 0,
            "page_matches": 0,
            "missing_items": [],
            "extra_items": [],
            "level_errors": [],
            "text_errors": [],
            "page_errors": []
        }
        
        # Create lookup dictionaries for easier comparison
        expected_items = {(self.normalize_text(item["text"]), item["page"]): item for item in expected_outline}
        actual_items = {(self.normalize_text(item["text"]), item["page"]): item for item in actual_outline}
        
        # Check each expected item
        for exp_item in expected_outline:
            exp_key = (self.normalize_text(exp_item["text"]), exp_item["page"])
            
            if exp_key in actual_items:
                act_item = actual_items[exp_key]
                
                # Count different types of matches
                if (exp_item["level"] == act_item["level"] and 
                    self.normalize_text(exp_item["text"]) == self.normalize_text(act_item["text"]) and
                    exp_item["page"] == act_item["page"]):
                    metrics["exact_matches"] += 1
                
                if exp_item["level"] == act_item["level"]:
                    metrics["level_matches"] += 1
                else:
                    metrics["level_errors"].append({
                        "text": exp_item["text"],
                        "expected_level": exp_item["level"],
                        "actual_level": act_item["level"]
                    })
                
                if self.normalize_text(exp_item["text"]) == self.normalize_text(act_item["text"]):
                    metrics["text_matches"] += 1
                else:
                    metrics["text_errors"].append({
                        "expected": exp_item["text"],
                        "actual": act_item["text"]
                    })
                
                if exp_item["page"] == act_item["page"]:
                    metrics["page_matches"] += 1
                else:
                    metrics["page_errors"].append({
                        "text": exp_item["text"],
                        "expected_page": exp_item["page"],
                        "actual_page": act_item["page"]
                    })
            else:
                metrics["missing_items"].append(exp_item)
        
        # Check for extra items in actual output
        for act_item in actual_outline:
            act_key = (self.normalize_text(act_item["text"]), act_item["page"])
            if act_key not in expected_items:
                metrics["extra_items"].append(act_item)
        
        return metrics
    
    def calculate_scores(self, metrics: Dict) -> Dict:
        """Calculate percentage scores from metrics"""
        total_expected = metrics["total_expected"]
        
        if total_expected == 0:
            return {"precision": 0, "recall": 0, "f1": 0, "exact_match_rate": 0}
        
        # Precision: correct items / total actual items
        precision = metrics["exact_matches"] / max(metrics["total_actual"], 1)
        
        # Recall: correct items / total expected items
        recall = metrics["exact_matches"] / total_expected
        
        # F1 Score
        f1 = 2 * (precision * recall) / max(precision + recall, 1e-10)
        
        # Exact match rate
        exact_match_rate = metrics["exact_matches"] / total_expected
        
        return {
            "precision": precision * 100,
            "recall": recall * 100,
            "f1": f1 * 100,
            "exact_match_rate": exact_match_rate * 100
        }
    
    def test_document(self, filename: str) -> Dict:
        """Test a single document and return results"""
        base_name = os.path.splitext(filename)[0]
        expected_file = os.path.join(self.expected_folder, f"{base_name}_outline.json")
        actual_file = os.path.join(self.actual_folder, f"{base_name}_outline.json")
        
        print(f"\n--- Testing {filename} ---")
        
        # Load expected and actual outputs
        expected = self.load_json_file(expected_file)
        actual = self.load_json_file(actual_file)
        
        if expected is None:
            return {"error": f"Could not load expected output: {expected_file}"}
        
        if actual is None:
            return {"error": f"Could not load actual output: {actual_file}"}
        
        # Compare titles
        title_match, title_message = self.compare_titles(expected, actual)
        
        # Compare outlines
        outline_metrics = self.compare_outlines(expected, actual)
        scores = self.calculate_scores(outline_metrics)
        
        result = {
            "filename": filename,
            "title_correct": title_match,
            "title_details": title_message,
            "outline_metrics": outline_metrics,
            "scores": scores,
            "success": True
        }
        
        return result
    
    def run_full_test(self) -> Dict:
        """Run complete accuracy test on all documents"""
        print("="*60)
        print("PDF Document Outline Extraction - Accuracy Test")
        print("="*60)
        
        # Run PDF processor
        if not self.run_pdf_processor():
            return {"error": "Failed to run PDF processor"}
        
        # Find test documents
        test_files = [f for f in os.listdir(self.test_pdfs_folder) if f.endswith('.pdf')]
        
        if not test_files:
            return {"error": f"No test PDF files found in {self.test_pdfs_folder}"}
        
        # Test each document
        all_results = {}
        total_scores = {"precision": [], "recall": [], "f1": [], "exact_match_rate": []}
        title_accuracy = []
        
        for filename in sorted(test_files):
            result = self.test_document(filename)
            all_results[filename] = result
            
            if result.get("success"):
                # Collect scores for averaging
                scores = result["scores"]
                total_scores["precision"].append(scores["precision"])
                total_scores["recall"].append(scores["recall"])
                total_scores["f1"].append(scores["f1"])
                total_scores["exact_match_rate"].append(scores["exact_match_rate"])
                
                title_accuracy.append(1 if result["title_correct"] else 0)
        
        # Calculate overall averages
        overall_scores = {}
        for metric, values in total_scores.items():
            overall_scores[metric] = sum(values) / len(values) if values else 0
        
        overall_title_accuracy = sum(title_accuracy) / len(title_accuracy) * 100 if title_accuracy else 0
        
        # Compile final results
        final_results = {
            "individual_results": all_results,
            "overall_scores": overall_scores,
            "title_accuracy": overall_title_accuracy,
            "documents_tested": len(test_files),
            "successful_tests": len([r for r in all_results.values() if r.get("success")])
        }
        
        return final_results
    
    def print_detailed_report(self, results: Dict):
        """Print a detailed accuracy report"""
        if "error" in results:
            print(f"Test failed: {results['error']}")
            return
        
        print(f"\n{'='*60}")
        print("DETAILED ACCURACY REPORT")
        print(f"{'='*60}")
        
        print(f"Documents tested: {results['documents_tested']}")
        print(f"Successful tests: {results['successful_tests']}")
        print(f"Title accuracy: {results['title_accuracy']:.1f}%")
        
        print(f"\nOVERALL OUTLINE ACCURACY:")
        print(f"  Precision:      {results['overall_scores']['precision']:.1f}%")
        print(f"  Recall:         {results['overall_scores']['recall']:.1f}%")
        print(f"  F1 Score:       {results['overall_scores']['f1']:.1f}%")
        print(f"  Exact Match:    {results['overall_scores']['exact_match_rate']:.1f}%")
        
        # Individual document details
        for filename, result in results["individual_results"].items():
            if not result.get("success"):
                print(f"\n❌ {filename}: {result.get('error', 'Unknown error')}")
                continue
                
            print(f"\n📄 {filename}:")
            print(f"  Title: {'✅' if result['title_correct'] else '❌'} {result['title_details']}")
            
            scores = result["scores"]
            print(f"  Outline Scores:")
            print(f"    Precision:    {scores['precision']:.1f}%")
            print(f"    Recall:       {scores['recall']:.1f}%")
            print(f"    F1 Score:     {scores['f1']:.1f}%")
            print(f"    Exact Match:  {scores['exact_match_rate']:.1f}%")
            
            metrics = result["outline_metrics"]
            print(f"  Details: {metrics['exact_matches']}/{metrics['total_expected']} exact matches")
            
            if metrics["missing_items"]:
                print(f"  Missing items: {len(metrics['missing_items'])}")
                for item in metrics["missing_items"][:3]:  # Show first 3
                    print(f"    - {item['level']}: {item['text']}")
            
            if metrics["extra_items"]:
                print(f"  Extra items: {len(metrics['extra_items'])}")
                for item in metrics["extra_items"][:3]:  # Show first 3
                    print(f"    + {item['level']}: {item['text']}")
            
            if metrics["level_errors"]:
                print(f"  Level errors: {len(metrics['level_errors'])}")
                for error in metrics["level_errors"][:3]:  # Show first 3
                    print(f"    ~ {error['text']}: {error['expected_level']} → {error['actual_level']}")
        
        # Summary
        print(f"\n{'='*60}")
        avg_f1 = results['overall_scores']['f1']
        if avg_f1 >= 90:
            grade = "Excellent 🌟"
        elif avg_f1 >= 80:
            grade = "Good 👍"
        elif avg_f1 >= 70:
            grade = "Fair 👌"
        elif avg_f1 >= 60:
            grade = "Needs Improvement 📈"
        else:
            grade = "Poor 😞"
            
        print(f"OVERALL PERFORMANCE: {grade}")
        print(f"Average F1 Score: {avg_f1:.1f}%")
        print(f"{'='*60}")

def main():
    parser = argparse.ArgumentParser(description="Test PDF outline extraction accuracy")
    parser.add_argument("--generate", action="store_true", help="Generate test PDFs first")
    parser.add_argument("--test-only", action="store_true", help="Run tests only (skip PDF generation)")
    args = parser.parse_args()
    
    if args.generate and not args.test_only:
        print("Generating test PDFs first...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, "generate_test_pdfs.py"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error generating test PDFs: {result.stderr}")
                return
            print("Test PDFs generated successfully")
        except Exception as e:
            print(f"Error running test PDF generator: {e}")
            return
    
    # Run accuracy test
    tester = AccuracyTester()
    results = tester.run_full_test()
    tester.print_detailed_report(results)
    
    # Save results to file
    output_file = "accuracy_test_results.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\nDetailed results saved to: {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    main()
