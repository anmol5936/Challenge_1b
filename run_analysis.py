#!/usr/bin/env python3

import json
import sys
import os
from datetime import datetime

# Simple test runner for the PDF analysis system
def create_sample_input():
    """Create a sample input for testing"""
    sample_input = {
        "challenge_info": {
            "challenge_id": "round_1b_test",
            "test_case_name": "sample_test",
            "description": "Sample test case for PDF analysis system"
        },
        "documents": [
            {
                "filename": "sample_document.pdf", 
                "title": "Sample Document"
            }
        ],
        "persona": {
            "role": "Travel planning specialist helping a group of 10 college friends plan their 4-day trip"
        },
        "job_to_be_done": {
            "task": "Plan a comprehensive 4-day itinerary for a group of 10 college friends, including accommodations, activities, and dining options"
        }
    }
    return sample_input

def main():
    print("Multi-Collection PDF Analysis System")
    print("=" * 50)
    
    # Import the main analyzer
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from main import MultiCollectionPDFAnalyzer
        
        # Create sample input if no input file provided
        if len(sys.argv) < 2:
            print("No input file provided. Creating sample input...")
            input_data = create_sample_input()
            documents_path = ""
        else:
            input_file = sys.argv[1]
            documents_path = sys.argv[2] if len(sys.argv) > 2 else ""
            
            with open(input_file, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
        
        # Create and run analyzer
        analyzer = MultiCollectionPDFAnalyzer()
        
        print(f"Processing input with {len(input_data.get('documents', []))} documents...")
        print(f"Persona: {input_data.get('persona', {}).get('role', 'Unknown')}")
        print(f"Task: {input_data.get('job_to_be_done', {}).get('task', 'Unknown')[:100]}...")
        print()
        
        # Process the collection
        start_time = datetime.now()
        result = analyzer.process_collection(input_data, documents_path)
        end_time = datetime.now()
        
        processing_time = (end_time - start_time).total_seconds()
        print(f"\nProcessing completed in {processing_time:.2f} seconds")
        
        # Display results summary
        if "error" in result.get("metadata", {}):
            print(f"ERROR: {result['metadata']['error']}")
        else:
            sections_count = len(result.get("extracted_sections", []))
            subsections_count = len(result.get("subsection_analysis", []))
            
            print(f"Extracted {sections_count} sections")
            print(f"Generated {subsections_count} refined subsections")
            
            if sections_count > 0:
                print("\nTop 3 Sections:")
                for i, section in enumerate(result["extracted_sections"][:3], 1):
                    print(f"  {i}. {section['section_title']} (Rank: {section['importance_rank']}, Page: {section['page_number']})")
        
        # Save output
        output_file = "analysis_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nFull output saved to: {output_file}")
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure all required dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error running analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()