#!/usr/bin/env python3
"""
Constitutional Test Runner for GDP Dashboard

This script runs all tests to ensure constitutional compliance across
all principles: AEGIS, PORTABILITÉ, HYGIE, and CHRONOS.
"""

import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

def run_constitutional_tests():
    """
    Run all constitutional compliance tests.
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("🏛️ Running Constitutional Compliance Tests for cerebrum-1")
    print("=" * 60)
    
    # Discover and run all tests
    test_dir = Path(__file__).parent
    loader = unittest.TestLoader()
    
    # Load tests from test directory
    test_suite = loader.discover(str(test_dir), pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    
    if result.wasSuccessful():
        print("✅ All constitutional tests passed!")
        print(f"Tests run: {result.testsRun}")
        print("🏛️ Repository complies with cerebrum-1 constitution")
        return True
    else:
        print("❌ Some tests failed!")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print("\n🚨 FAILURES:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print("\n🚨 ERRORS:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback.split()[-1] if traceback.split() else 'Unknown error'}")
        
        print("\n⚖️ Constitutional compliance violations detected!")
        return False

def validate_constitutional_structure():
    """
    Validate that the repository follows constitutional structure requirements.
    
    Returns:
        bool: True if structure is compliant
    """
    print("\n🏗️ Validating Constitutional Structure")
    print("-" * 40)
    
    repo_root = Path(__file__).parent.parent
    required_dirs = ['src', 'docs', 'tests', 'prompts']
    required_files = [
        'docs/CONSTITUTION.md',
        'docs/WORKFLOW.md',
        'src/gdp_core.py',
        'src/gdp_ui.py',
        'tests/test_gdp_core.py',
        'tests/test_integration.py'
    ]
    
    structure_valid = True
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = repo_root / dir_name
        if dir_path.exists():
            print(f"✅ Directory exists: {dir_name}/")
        else:
            print(f"❌ Missing directory: {dir_name}/")
            structure_valid = False
    
    # Check files
    for file_path in required_files:
        full_path = repo_root / file_path
        if full_path.exists():
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            structure_valid = False
    
    if structure_valid:
        print("✅ Constitutional structure validated")
    else:
        print("❌ Constitutional structure violations detected")
    
    return structure_valid

def main():
    """Main test runner entry point."""
    print("🏛️ CONSTITUTIONAL COMPLIANCE VALIDATION")
    print("Repository: cerebrum-1 | GDP Dashboard")
    print("=" * 60)
    
    # Validate structure first
    structure_ok = validate_constitutional_structure()
    
    if not structure_ok:
        print("\n🚨 Structure validation failed - cannot proceed with tests")
        return False
    
    # Run all tests
    tests_ok = run_constitutional_tests()
    
    print("\n" + "=" * 60)
    print("📋 CONSTITUTIONAL COMPLIANCE SUMMARY")
    print("=" * 60)
    
    if structure_ok and tests_ok:
        print("✅ Repository is fully compliant with cerebrum-1 constitution")
        print("✅ All principles validated:")
        print("   🛡️  AEGIS (Security): Environment-based config, no secrets")
        print("   🌐 PORTABILITÉ (Portability): Cross-platform, open standards")
        print("   🏥 HYGIE (Resilience): Comprehensive testing, error handling")
        print("   ⏱️  CHRONOS (Efficiency): Optimized processing, caching")
        return True
    else:
        print("❌ Repository has constitutional compliance issues")
        print("🔧 Review failures and ensure all principles are followed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)