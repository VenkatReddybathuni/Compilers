from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

from test_framework import TestResult
import unit_tests
import project_euler_tests
import error_tests

def run_all_tests():
    print("Running All Test Suites\n" + "=" * 50)
    
    # Run Unit Tests
    print("\nRunning Unit Tests:")
    print("-" * 30)
    unit_tests.run_tests()
    
    # Run Project Euler Tests
    print("\nRunning Project Euler Tests:")
    print("-" * 30)
    project_euler_tests.run_tests()
    
    # Run Error Tests (these are expected to fail)
    print("\nRunning Error Tests (Expected to Fail):")
    print("-" * 30)
    print("Note: These tests are designed to verify error handling - failures are expected")
    error_tests.run_tests()
    
    print("\n" + "=" * 50)
    print("All test suites completed")

if __name__ == "__main__":
    run_all_tests()
