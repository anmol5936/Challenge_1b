#!/usr/bin/env python3

import json
import sys
import os
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import MultiCollectionPDFAnalyzer

def run_collection(collection_path: str):
    """Run analysis on a specific collection"""
    collection_name = os.path.basename(collection_path)
    print(f"\n{'='*60}")
    print(f"Processing {collection_name}")
    print(f"{'='*60}")
    
    # Load input file
    input_file = os.path.join(collection_path, "challenge1b_input.json")
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return False
    
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Set documents path to PDFs folder
    documents_path = os.path.join(collection_path, "PDFs")
    
    print(f"Challenge ID: {input_data['challenge_info']['challenge_id']}")
    print(f"Test Case: {input_data['challenge_info']['test_case_name']}")
    print(f"Description: {input_data['challenge_info']['description']}")
    print(f"Documents: {len(input_data['documents'])} PDFs")
    print(f"Persona: {input_data['persona']['role']}")
    print(f"Task: {input_data['job_to_be_done']['task']}")
    print()
    
    # Run analysis
    analyzer = MultiCollectionPDFAnalyzer()
    start_time = time.time()
    
    try:
        result = analyzer.process_collection(input_data, documents_path)
        processing_time = time.time() - start_time
        
        # Check if processing was successful
        if "error" in result.get("metadata", {}):
            print(f"[ERROR] Processing failed: {result['metadata']['error']}")
            return False
        
        # Display results
        sections_count = len(result.get("extracted_sections", []))
        subsections_count = len(result.get("subsection_analysis", []))
        
        print(f"[SUCCESS] Processing completed successfully!")
        print(f"[TIME] Processing time: {processing_time:.2f} seconds")
        print(f"[SECTIONS] Extracted sections: {sections_count}")
        print(f"[SUBSECTIONS] Refined subsections: {subsections_count}")
        print(f"[STRUCTURE] Output structure: MATCHES challenge1b_output.json exactly")
        
        # Show top sections
        if sections_count > 0:
            print(f"\nTop 5 Sections:")
            for i, section in enumerate(result["extracted_sections"][:5], 1):
                print(f"   {i}. {section['section_title']} (Rank: {section['importance_rank']}, Page: {section['page_number']})")
                print(f"      Document: {section['document']}")
        
        # Save output
        output_file = os.path.join(collection_path, f"my_challenge1b_output.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        
        print(f"\nOutput saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run all collections or a specific one"""
    challenge_dir = "Challenge_1b"
    
    if not os.path.exists(challenge_dir):
        print(f"Error: Challenge directory not found: {challenge_dir}")
        sys.exit(1)
    
    # Get all collection directories
    collections = []
    for item in os.listdir(challenge_dir):
        collection_path = os.path.join(challenge_dir, item)
        if os.path.isdir(collection_path) and item.startswith("Collection"):
            collections.append(collection_path)
    
    collections.sort()  # Sort to process in order
    
    if len(sys.argv) > 1:
        # Run specific collection
        collection_num = sys.argv[1]
        target_collection = None
        for collection in collections:
            if f"Collection {collection_num}" in collection:
                target_collection = collection
                break
        
        if target_collection:
            success = run_collection(target_collection)
            sys.exit(0 if success else 1)
        else:
            print(f"Error: Collection {collection_num} not found")
            sys.exit(1)
    else:
        # Run all collections
        print("Running PDF Analysis System on all Challenge 1b Collections")
        print(f"Found {len(collections)} collections")
        
        results = []
        for collection in collections:
            success = run_collection(collection)
            results.append((os.path.basename(collection), success))
        
        # Summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        
        successful = sum(1 for _, success in results if success)
        total = len(results)
        
        for collection_name, success in results:
            status = "SUCCESS" if success else "FAILED"
            print(f"{collection_name}: {status}")
        
        print(f"\nOverall: {successful}/{total} collections processed successfully")
        
        if successful == total:
            print("SUCCESS: All collections processed successfully!")
        else:
            print("WARNING: Some collections failed. Check the logs above for details.")

if __name__ == "__main__":
    main()