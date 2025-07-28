#!/usr/bin/env python3

import os
import re
from typing import List, Dict, Any

def check_dockerfile_syntax() -> Dict[str, Any]:
    """Check Dockerfile for common issues and best practices"""
    results = {
        'valid': True,
        'warnings': [],
        'errors': [],
        'best_practices': []
    }
    
    if not os.path.exists('Dockerfile'):
        results['valid'] = False
        results['errors'].append("Dockerfile not found")
        return results
    
    with open('Dockerfile', 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Check for required instructions
    required_instructions = ['FROM', 'WORKDIR', 'COPY', 'CMD']
    for instruction in required_instructions:
        if not re.search(f'^{instruction}', content, re.MULTILINE):
            results['errors'].append(f"Missing required instruction: {instruction}")
    
    # Check for best practices
    if 'apt-get update' in content and 'apt-get clean' not in content:
        results['warnings'].append("Consider adding 'apt-get clean' after 'apt-get update'")
    
    if 'pip install' in content and '--no-cache-dir' not in content:
        results['warnings'].append("Consider using '--no-cache-dir' with pip install")
    
    if 'USER root' in content or 'USER 0' in content:
        results['warnings'].append("Running as root user - consider using non-root user")
    
    # Check for security best practices
    if 'USER app' in content:
        results['best_practices'].append("✓ Using non-root user")
    
    if 'HEALTHCHECK' in content:
        results['best_practices'].append("✓ Health check configured")
    
    if '--no-cache-dir' in content:
        results['best_practices'].append("✓ Using pip --no-cache-dir")
    
    if 'rm -rf /var/lib/apt/lists/*' in content:
        results['best_practices'].append("✓ Cleaning apt cache")
    
    return results

def check_required_files() -> Dict[str, Any]:
    """Check if all required files are present"""
    results = {
        'valid': True,
        'missing_files': [],
        'present_files': []
    }
    
    required_files = [
        'requirements.txt',
        'src/main.py',
        'run_challenge.py',
        'analyze_compliance.py',
        'verify_exact_structure.py',
        'Challenge_1b/Collection 1/challenge1b_input.json',
        'Challenge_1b/Collection 2/challenge1b_input.json',
        'Challenge_1b/Collection 3/challenge1b_input.json'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            results['present_files'].append(file_path)
        else:
            results['missing_files'].append(file_path)
            results['valid'] = False
    
    return results

def check_dockerignore() -> Dict[str, Any]:
    """Check .dockerignore file"""
    results = {
        'exists': os.path.exists('.dockerignore'),
        'recommendations': []
    }
    
    if results['exists']:
        with open('.dockerignore', 'r') as f:
            content = f.read()
        
        recommended_ignores = [
            '__pycache__',
            '.git',
            'node_modules',
            '*.log',
            '.env'
        ]
        
        for ignore in recommended_ignores:
            if ignore in content:
                results['recommendations'].append(f"✓ Ignoring {ignore}")
            else:
                results['recommendations'].append(f"⚠ Consider ignoring {ignore}")
    else:
        results['recommendations'].append("Consider creating .dockerignore file")
    
    return results

def validate_docker_compose() -> Dict[str, Any]:
    """Validate docker-compose.yml"""
    results = {
        'exists': os.path.exists('docker-compose.yml'),
        'services': [],
        'issues': []
    }
    
    if results['exists']:
        try:
            import yaml
            with open('docker-compose.yml', 'r') as f:
                compose_data = yaml.safe_load(f)
            
            if 'services' in compose_data:
                results['services'] = list(compose_data['services'].keys())
            
            # Check for volume mounts
            has_volumes = any('volumes' in service for service in compose_data.get('services', {}).values())
            if has_volumes:
                results['issues'].append("✓ Volume mounts configured")
            else:
                results['issues'].append("⚠ No volume mounts found")
                
        except ImportError:
            results['issues'].append("⚠ PyYAML not available for validation")
        except Exception as e:
            results['issues'].append(f"❌ Error parsing docker-compose.yml: {e}")
    
    return results

def main():
    """Main validation function"""
    print("Docker Configuration Validation")
    print("=" * 50)
    
    # Check Dockerfile
    print("\n📄 Dockerfile Analysis:")
    dockerfile_results = check_dockerfile_syntax()
    
    if dockerfile_results['valid']:
        print("SUCCESS: Dockerfile syntax is valid")
    else:
        print("❌ Dockerfile has issues")
    
    for error in dockerfile_results['errors']:
        print(f"   ❌ Error: {error}")
    
    for warning in dockerfile_results['warnings']:
        print(f"   ⚠️  Warning: {warning}")
    
    for bp in dockerfile_results['best_practices']:
        print(f"   {bp}")
    
    # Check required files
    print("\n📁 Required Files Check:")
    files_results = check_required_files()
    
    if files_results['valid']:
        print("SUCCESS: All required files are present")
    else:
        print("❌ Some required files are missing")
    
    print(f"   Present files: {len(files_results['present_files'])}")
    for missing in files_results['missing_files']:
        print(f"   ❌ Missing: {missing}")
    
    # Check .dockerignore
    print("\n.dockerignore Analysis:")
    ignore_results = check_dockerignore()
    
    if ignore_results['exists']:
        print("SUCCESS: .dockerignore file exists")
        for rec in ignore_results['recommendations']:
            print(f"   {rec}")
    else:
        print("⚠️  .dockerignore file not found")
    
    # Check docker-compose.yml
    print("\nDocker Compose Analysis:")
    compose_results = validate_docker_compose()
    
    if compose_results['exists']:
        print("SUCCESS: docker-compose.yml exists")
        print(f"   Services: {', '.join(compose_results['services'])}")
        for issue in compose_results['issues']:
            print(f"   {issue}")
    else:
        print("⚠️  docker-compose.yml not found")
    
    # Overall assessment
    print("\nOverall Assessment:")
    
    overall_valid = (
        dockerfile_results['valid'] and 
        files_results['valid'] and
        len(dockerfile_results['errors']) == 0
    )
    
    if overall_valid:
        print("SUCCESS: Docker configuration is ready for use!")
        print("\nNext steps:")
        print("   1. Start Docker Desktop")
        print("   2. Run: python docker_setup.py build")
        print("   3. Run: docker run --rm pdf-analysis-system")
    else:
        print("❌ Docker configuration needs attention")
        print("   Please fix the issues above before building")
    
    return overall_valid

if __name__ == "__main__":
    main()