#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import time

def run_test(command, description, timeout=120):
    """Run a test command with timeout"""
    print(f"🧪 {description}...")
    try:
        start_time = time.time()
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        end_time = time.time()
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED ({end_time - start_time:.2f}s)")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT ({timeout}s)")
        return False
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {e}")
        return False

def check_output_files():
    """Check if output files are generated correctly"""
    print("📁 Checking output files...")
    
    expected_files = [
        "Challenge_1b/Collection 1/my_challenge1b_output.json",
        "Challenge_1b/Collection 2/my_challenge1b_output.json",
        "Challenge_1b/Collection 3/my_challenge1b_output.json"
    ]
    
    all_exist = True
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
            
            # Check if it's valid JSON
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Check required structure
                required_keys = ['metadata', 'extracted_sections', 'subsection_analysis']
                for key in required_keys:
                    if key not in data:
                        print(f"   ❌ Missing key '{key}' in {file_path}")
                        all_exist = False
                    else:
                        print(f"      ✓ {key}")
                        
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON in {file_path}: {e}")
                all_exist = False
        else:
            print(f"   ❌ Missing: {file_path}")
            all_exist = False
    
    return all_exist

def main():
    """Run comprehensive system tests"""
    print("🚀 Complete System Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Component imports
    total_tests += 1
    if run_test("python -c \"import sys; sys.path.insert(0, 'src'); from main import MultiCollectionPDFAnalyzer; print('All imports successful')\"", 
                "Component imports test"):
        tests_passed += 1
    
    # Test 2: Individual collection processing
    for i in range(1, 4):
        total_tests += 1
        if run_test(f"python run_challenge.py {i}", f"Collection {i} processing"):
            tests_passed += 1
    
    # Test 3: Check output files
    total_tests += 1
    if check_output_files():
        print("✅ Output files validation - PASSED")
        tests_passed += 1
    else:
        print("❌ Output files validation - FAILED")
    
    # Test 4: Structure compliance
    total_tests += 1
    if run_test("python analyze_compliance.py", "Structure compliance check"):
        tests_passed += 1
    
    # Test 5: Exact structure verification
    total_tests += 1
    if run_test("python verify_exact_structure.py", "Exact structure verification"):
        tests_passed += 1
    
    # Test 6: Docker configuration validation
    total_tests += 1
    if run_test("python validate_docker.py", "Docker configuration validation"):
        tests_passed += 1
    
    # Test 7: All collections processing
    total_tests += 1
    if run_test("python run_challenge.py", "All collections processing", timeout=180):
        tests_passed += 1
    
    # Results summary
    print(f"\n{'='*60}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready for production use")
        print("✅ Challenge 1b requirements fully met")
        
        # Show final performance summary
        print(f"\n📈 PERFORMANCE SUMMARY:")
        try:
            # Get file sizes
            for i in range(1, 4):
                file_path = f"Challenge_1b/Collection {i}/my_challenge1b_output.json"
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    sections = len(data.get('extracted_sections', []))
                    subsections = len(data.get('subsection_analysis', []))
                    print(f"   Collection {i}: {sections} sections, {subsections} subsections ({size} bytes)")
        except Exception as e:
            print(f"   Could not generate performance summary: {e}")
        
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Please review the failed tests above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)