#!/usr/bin/env python3

import json
import os
from typing import Dict, List, Any

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def check_structure_compliance(expected: Dict[str, Any], actual: Dict[str, Any]) -> Dict[str, Any]:
    """Check compliance between expected and actual output structures"""
    compliance = {
        'metadata': {'score': 0, 'max': 4, 'details': []},
        'extracted_sections': {'score': 0, 'max': 4, 'details': []},
        'subsection_analysis': {'score': 0, 'max': 3, 'details': []},
        'overall': {'score': 0, 'max': 11}
    }
    
    # Check metadata structure
    if 'metadata' in actual:
        meta_actual = actual['metadata']
        meta_expected = expected.get('metadata', {})
        
        # Check required fields
        required_meta_fields = ['input_documents', 'persona', 'job_to_be_done', 'processing_timestamp']
        for field in required_meta_fields:
            if field in meta_actual:
                compliance['metadata']['score'] += 1
                compliance['metadata']['details'].append(f"✓ {field} present")
            else:
                compliance['metadata']['details'].append(f"✗ {field} missing")
        
        # Check input_documents format
        if 'input_documents' in meta_actual:
            if isinstance(meta_actual['input_documents'], list):
                if len(meta_actual['input_documents']) > 0:
                    if isinstance(meta_actual['input_documents'][0], str):
                        compliance['metadata']['details'].append("✓ input_documents format correct (list of strings)")
                    else:
                        compliance['metadata']['details'].append("✗ input_documents should be list of strings")
    else:
        compliance['metadata']['details'].append("✗ metadata section missing")
    
    # Check extracted_sections structure
    if 'extracted_sections' in actual:
        sections_actual = actual['extracted_sections']
        if isinstance(sections_actual, list):
            compliance['extracted_sections']['score'] += 1
            compliance['extracted_sections']['details'].append("✓ extracted_sections is array")
            
            if len(sections_actual) > 0:
                compliance['extracted_sections']['score'] += 1
                compliance['extracted_sections']['details'].append(f"✓ Has {len(sections_actual)} sections")
                
                # Check section structure
                section = sections_actual[0]
                required_section_fields = ['document', 'section_title', 'importance_rank', 'page_number']
                section_fields_present = sum(1 for field in required_section_fields if field in section)
                
                if section_fields_present == len(required_section_fields):
                    compliance['extracted_sections']['score'] += 2
                    compliance['extracted_sections']['details'].append("✓ Section structure complete")
                else:
                    compliance['extracted_sections']['score'] += 1
                    compliance['extracted_sections']['details'].append(f"⚠ Section structure partial ({section_fields_present}/{len(required_section_fields)} fields)")
            else:
                compliance['extracted_sections']['details'].append("✗ No sections extracted")
        else:
            compliance['extracted_sections']['details'].append("✗ extracted_sections is not array")
    else:
        compliance['extracted_sections']['details'].append("✗ extracted_sections missing")
    
    # Check subsection_analysis structure
    if 'subsection_analysis' in actual:
        subsections_actual = actual['subsection_analysis']
        if isinstance(subsections_actual, list):
            compliance['subsection_analysis']['score'] += 1
            compliance['subsection_analysis']['details'].append("✓ subsection_analysis is array")
            
            if len(subsections_actual) > 0:
                compliance['subsection_analysis']['score'] += 1
                compliance['subsection_analysis']['details'].append(f"✓ Has {len(subsections_actual)} subsections")
                
                # Check subsection structure
                subsection = subsections_actual[0]
                required_subsection_fields = ['document', 'refined_text', 'page_number']
                subsection_fields_present = sum(1 for field in required_subsection_fields if field in subsection)
                
                if subsection_fields_present == len(required_subsection_fields):
                    compliance['subsection_analysis']['score'] += 1
                    compliance['subsection_analysis']['details'].append("✓ Subsection structure complete")
                else:
                    compliance['subsection_analysis']['details'].append(f"⚠ Subsection structure partial ({subsection_fields_present}/{len(required_subsection_fields)} fields)")
            else:
                compliance['subsection_analysis']['details'].append("✗ No subsections generated")
        else:
            compliance['subsection_analysis']['details'].append("✗ subsection_analysis is not array")
    else:
        compliance['subsection_analysis']['details'].append("✗ subsection_analysis missing")
    
    # Calculate overall score
    compliance['overall']['score'] = (
        compliance['metadata']['score'] + 
        compliance['extracted_sections']['score'] + 
        compliance['subsection_analysis']['score']
    )
    
    return compliance

def analyze_all_collections():
    """Analyze compliance for all collections"""
    collections = []
    total_score = 0
    max_total_score = 0
    
    print("PDF Analysis System - Structure Compliance Analysis")
    print("=" * 60)
    
    for i in range(1, 4):
        collection_path = f"Challenge_1b/Collection {i}"
        expected_file = os.path.join(collection_path, "challenge1b_output.json")
        actual_file = os.path.join(collection_path, "my_challenge1b_output.json")
        
        if os.path.exists(expected_file) and os.path.exists(actual_file):
            expected = load_json_file(expected_file)
            actual = load_json_file(actual_file)
            
            if expected and actual:
                compliance = check_structure_compliance(expected, actual)
                collections.append({
                    'id': i,
                    'compliance': compliance
                })
                
                score = compliance['overall']['score']
                max_score = compliance['overall']['max']
                percentage = (score / max_score) * 100
                
                total_score += score
                max_total_score += max_score
                
                print(f"\n📊 Collection {i} Analysis:")
                print(f"   Overall Score: {score}/{max_score} ({percentage:.1f}%)")
                
                # Show detailed breakdown
                for section, data in compliance.items():
                    if section != 'overall':
                        section_score = data['score']
                        section_max = data['max']
                        section_pct = (section_score / section_max) * 100 if section_max > 0 else 0
                        print(f"   {section.replace('_', ' ').title()}: {section_score}/{section_max} ({section_pct:.1f}%)")
                        
                        for detail in data['details']:
                            print(f"     {detail}")
            else:
                print(f"\n❌ Collection {i}: Failed to load files")
        else:
            print(f"\n❌ Collection {i}: Files not found")
            print(f"     Expected: {expected_file}")
            print(f"     Actual: {actual_file}")
    
    # Overall summary
    if max_total_score > 0:
        overall_percentage = (total_score / max_total_score) * 100
        print(f"\n{'='*60}")
        print(f"📈 OVERALL COMPLIANCE SUMMARY")
        print(f"{'='*60}")
        print(f"Total Score: {total_score}/{max_total_score} ({overall_percentage:.1f}%)")
        print(f"Collections Analyzed: {len(collections)}")
        
        if overall_percentage >= 90:
            print("EXCELLENT: System meets challenge requirements.")
        elif overall_percentage >= 75:
            print("GOOD: Minor improvements needed.")
        elif overall_percentage >= 50:
            print("MODERATE: Several issues need attention.")
        else:
            print("POOR: Major structural issues need fixing.")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        # Analyze common issues
        metadata_issues = []
        section_issues = []
        subsection_issues = []
        
        for collection in collections:
            comp = collection['compliance']
            if comp['metadata']['score'] < comp['metadata']['max']:
                metadata_issues.extend([d for d in comp['metadata']['details'] if d.startswith('✗')])
            if comp['extracted_sections']['score'] < comp['extracted_sections']['max']:
                section_issues.extend([d for d in comp['extracted_sections']['details'] if d.startswith('✗')])
            if comp['subsection_analysis']['score'] < comp['subsection_analysis']['max']:
                subsection_issues.extend([d for d in comp['subsection_analysis']['details'] if d.startswith('✗')])
        
        if metadata_issues:
            print("   - Fix metadata structure issues")
        if section_issues:
            print("   - Improve section extraction and formatting")
        if subsection_issues:
            print("   - Enhance subsection analysis quality")
        
        print("   - Ensure all required fields are present in output")
        print("   - Validate JSON structure matches expected format exactly")
        
    return collections, overall_percentage

if __name__ == "__main__":
    analyze_all_collections()