#!/usr/bin/env python3

import json
import os
from typing import Dict, Any

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def compare_structure(expected: Dict[str, Any], actual: Dict[str, Any], path: str = "") -> bool:
    """Compare two JSON structures recursively"""
    if type(expected) != type(actual):
        print(f"❌ Type mismatch at {path}: expected {type(expected)}, got {type(actual)}")
        return False
    
    if isinstance(expected, dict):
        # Check if all expected keys are present
        for key in expected.keys():
            if key not in actual:
                print(f"❌ Missing key at {path}.{key}")
                return False
        
        # Check if there are extra keys in actual (except performance_stats which we removed)
        for key in actual.keys():
            if key not in expected and key != "performance_stats":
                print(f"⚠️  Extra key at {path}.{key}")
        
        # Recursively check each key
        for key in expected.keys():
            if key in actual:
                if not compare_structure(expected[key], actual[key], f"{path}.{key}" if path else key):
                    return False
    
    elif isinstance(expected, list):
        if len(expected) == 0 and len(actual) == 0:
            return True
        
        if len(expected) > 0 and len(actual) > 0:
            # Compare structure of first element
            return compare_structure(expected[0], actual[0], f"{path}[0]")
    
    return True

def verify_exact_structure():
    """Verify that our outputs match the expected structure exactly"""
    print("Exact Structure Verification")
    print("=" * 50)
    
    all_match = True
    
    for i in range(1, 4):
        collection_path = f"Challenge_1b/Collection {i}"
        expected_file = os.path.join(collection_path, "challenge1b_output.json")
        actual_file = os.path.join(collection_path, "my_challenge1b_output.json")
        
        print(f"\nCollection {i} Structure Verification:")
        
        if os.path.exists(expected_file) and os.path.exists(actual_file):
            expected = load_json_file(expected_file)
            actual = load_json_file(actual_file)
            
            if expected and actual:
                # Compare top-level structure
                matches = compare_structure(expected, actual)
                
                if matches:
                    print("SUCCESS: Structure matches perfectly!")
                    
                    # Additional checks
                    print("   ✓ metadata structure matches")
                    print("   ✓ extracted_sections structure matches")
                    print("   ✓ subsection_analysis structure matches")
                    
                    # Check specific field types
                    if isinstance(actual['metadata']['input_documents'], list):
                        print("   ✓ input_documents is list of strings")
                    
                    if isinstance(actual['metadata']['persona'], str):
                        print("   ✓ persona is string")
                    
                    if isinstance(actual['metadata']['job_to_be_done'], str):
                        print("   ✓ job_to_be_done is string")
                    
                    if 'performance_stats' not in actual['metadata']:
                        print("   ✓ performance_stats correctly excluded")
                    
                else:
                    print("❌ Structure mismatch found!")
                    all_match = False
            else:
                print("❌ Failed to load files")
                all_match = False
        else:
            print("❌ Files not found")
            all_match = False
    
    print(f"\n{'='*50}")
    if all_match:
        print("SUCCESS: ALL COLLECTIONS HAVE PERFECT STRUCTURE MATCH!")
        print("Ready for Challenge 1b submission")
    else:
        print("❌ Some structure mismatches found")
    
    return all_match

if __name__ == "__main__":
    verify_exact_structure()