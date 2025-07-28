#!/usr/bin/env python3

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    print("🐳 Checking Docker setup...")
    
    # Check if Docker is installed
    if not run_command("docker --version", "Checking Docker installation"):
        print("❌ Docker is not installed. Please install Docker Desktop first.")
        return False
    
    # Check if Docker is running
    if not run_command("docker info", "Checking Docker daemon"):
        print("❌ Docker daemon is not running. Please start Docker Desktop.")
        return False
    
    return True

def build_image():
    """Build the Docker image"""
    print("\n🏗️  Building Docker image...")
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Build the image
    if run_command("docker build -t pdf-analysis-system .", "Building Docker image"):
        print("✅ Docker image built successfully")
        return True
    else:
        print("❌ Failed to build Docker image")
        return False

def test_container():
    """Test the container"""
    print("\n🧪 Testing container...")
    
    # Test basic functionality
    test_commands = [
        ("docker run --rm pdf-analysis-system python -c \"import sys; sys.path.insert(0, 'src'); from main import MultiCollectionPDFAnalyzer; print('Import test passed')\"", 
         "Testing Python imports"),
        ("docker run --rm pdf-analysis-system python verify_exact_structure.py", 
         "Testing structure verification"),
    ]
    
    for command, description in test_commands:
        if not run_command(command, description):
            return False
    
    return True

def run_analysis():
    """Run the full analysis"""
    print("\n🚀 Running PDF analysis...")
    
    # Run all collections
    if run_command("docker run --rm -v $(pwd)/output:/app/output pdf-analysis-system python run_challenge.py", 
                   "Running all collections"):
        print("✅ Analysis completed successfully")
        
        # Run compliance check
        run_command("docker run --rm pdf-analysis-system python analyze_compliance.py", 
                   "Running compliance check")
        
        return True
    else:
        print("❌ Analysis failed")
        return False

def show_usage():
    """Show usage instructions"""
    print("\n📖 Docker Usage Instructions:")
    print("=" * 50)
    print("1. Build image:")
    print("   docker build -t pdf-analysis-system .")
    print()
    print("2. Run all collections:")
    print("   docker run --rm pdf-analysis-system")
    print()
    print("3. Run specific collection:")
    print("   docker run --rm pdf-analysis-system python run_challenge.py 1")
    print("   docker run --rm pdf-analysis-system python run_challenge.py 2")
    print("   docker run --rm pdf-analysis-system python run_challenge.py 3")
    print()
    print("4. Run compliance check:")
    print("   docker run --rm pdf-analysis-system python analyze_compliance.py")
    print()
    print("5. Verify structure:")
    print("   docker run --rm pdf-analysis-system python verify_exact_structure.py")
    print()
    print("6. Using Docker Compose:")
    print("   docker-compose up                    # Run all collections")
    print("   docker-compose --profile collection up pdf-analysis-collection1")
    print("   docker-compose --profile test up pdf-analysis-compliance")
    print()
    print("7. With volume mounting for output:")
    print("   docker run --rm -v $(pwd)/output:/app/output pdf-analysis-system")

def main():
    """Main setup function"""
    print("🐳 PDF Analysis System - Docker Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            if check_docker():
                build_image()
        elif sys.argv[1] == "test":
            if check_docker():
                test_container()
        elif sys.argv[1] == "run":
            if check_docker():
                run_analysis()
        elif sys.argv[1] == "usage":
            show_usage()
        else:
            print("Usage: python docker_setup.py [build|test|run|usage]")
    else:
        # Full setup
        if check_docker():
            if build_image():
                if test_container():
                    print("\n🎉 Docker setup completed successfully!")
                    show_usage()
                else:
                    print("\n❌ Container tests failed")
            else:
                print("\n❌ Image build failed")
        else:
            print("\n❌ Docker setup check failed")

if __name__ == "__main__":
    main()