from dataclasses import dataclass
from typing import Any, Optional
import sys
from io import StringIO
from contextlib import contextmanager
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main import e, parse, ParseError, TypeError

@dataclass
class TestCase:
    name: str
    code: str
    expected_output: Optional[str] = None  # For successful cases
    expected_error: Optional[type] = None  # For error cases
    env: list = None

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.results = []

    def add_result(self, test_name: str, passed: bool, message: str):
        self.total += 1
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        self.results.append((test_name, passed, message))

    def print_summary(self):
        print("\n=== Test Summary ===")
        print(f"Total Tests: {self.total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print("\nDetailed Results:")
        for name, passed, message in self.results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {name}")
            if not passed:
                print(f"    {message}")
        print("=" * 20)

@contextmanager
def capture_stdout():
    """Capture stdout for testing"""
    old_stdout = sys.stdout
    stdout = StringIO()
    sys.stdout = stdout
    try:
        yield stdout
    finally:
        sys.stdout = old_stdout

def run_test_case(test_case: TestCase) -> tuple[bool, str]:
    """Run a single test case and return (passed, message)"""
    try:
        with capture_stdout() as output:
            e(parse(test_case.code), test_case.env)
        actual_output = output.getvalue().strip()

        # If we have expected output, verify it matches
        if test_case.expected_output is not None:
            expected = test_case.expected_output.strip()
            if actual_output != expected:
                return False, f"Output mismatch\nExpected: {expected}\nGot: {actual_output}"

        return True, "Test passed successfully"

    except Exception as err:
        # Any error results in a failed test with the error message
        return False, f"Error: {type(err).__name__}: {str(err)}"

def run_test_suite(test_cases: list[TestCase]) -> TestResult:
    """Run a suite of test cases and return results"""
    results = TestResult()
    
    for test in test_cases:
        passed, message = run_test_case(test)
        results.add_result(test.name, passed, message)
        
    return results
