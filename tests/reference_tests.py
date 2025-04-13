from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from main import parse, e, BytecodeCompiler, BytecodeVM
from tests.test_framework import capture_stdout
import inspect
import time
from dataclasses import dataclass
from typing import List, Callable, Any, Dict

@dataclass
class ReferenceTest:
    """A test that compares our language with a reference Python implementation"""
    name: str
    description: str
    language_code: str
    reference_implementation: Callable
    test_cases: List[Any]  # Inputs to pass to both implementations
    compile_to_bytecode: bool = True  # Whether to compile to bytecode or use interpreter

@dataclass
class TestResult:
    """Results from running a single test case"""
    success: bool
    language_output: str
    reference_output: str
    execution_time_ms: float
    error_message: str = None

class ReferenceTestRunner:
    """Runs tests comparing language implementation with Python reference code"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.results = {}
        
    def run_test(self, test: ReferenceTest) -> Dict[Any, TestResult]:
        """Run a reference test with all its test cases"""
        self.log(f"\n== Running Test: {test.name} ==")
        self.log(f"Description: {test.description}")
        
        if self.verbose:
            self.log("\nLanguage Code:")
            for i, line in enumerate(test.language_code.strip().split('\n')):
                self.log(f"{i+1}: {line}")
            
            self.log("\nReference Implementation:")
            source = inspect.getsource(test.reference_implementation)
            for i, line in enumerate(source.strip().split('\n')):
                self.log(f"{i+1}: {line}")
        
        # Parse the language code once to avoid repeating that work
        try:
            ast = parse(test.language_code)
            if test.compile_to_bytecode:
                compiler = BytecodeCompiler()
                bytecode = compiler.compile(ast)
        except Exception as e:
            self.log(f"\nERROR: Failed to parse or compile the language code: {str(e)}")
            return {case: TestResult(False, "", "", 0, f"Failed to parse code: {str(e)}") 
                    for case in test.test_cases}
        
        results = {}
        for i, test_case in enumerate(test.test_cases):
            self.log(f"\nTest Case {i+1}: Input = {test_case}")
            result = self._run_case(test, test_case, ast, bytecode if test.compile_to_bytecode else None)
            results[test_case] = result
            
            status = "PASSED" if result.success else "FAILED"
            self.log(f"Case {i+1} Result: {status}")
            if not result.success:
                self.log(f"  Expected: {result.reference_output}")
                self.log(f"  Got: {result.language_output}")
                self.log(f"  Error: {result.error_message}")
            self.log(f"  Execution time: {result.execution_time_ms:.2f}ms")
        
        # Store results for this test
        self.results[test.name] = results
        return results
    
    def _run_case(self, test: ReferenceTest, test_case, ast, bytecode=None) -> TestResult:
        """Run a single test case comparing language output with reference implementation"""
        # Import e here to avoid circular imports
        from main import e
        
        # Run the reference implementation
        try:
            ref_start = time.time()
            reference_result = test.reference_implementation(test_case)
            ref_end = time.time()
            reference_output = str(reference_result).strip()
            ref_time_ms = (ref_end - ref_start) * 1000
        except Exception as ex:
            return TestResult(
                False, "", "", 0, 
                f"Reference implementation failed: {type(ex).__name__}: {str(ex)}"
            )
        
        # Run our language implementation
        try:
            # Create a variable binding for the input parameter
            if isinstance(test_case, tuple):
                # For tuple inputs (like pairs of numbers), convert to a list
                input_list = list(test_case)
                env = [("input", input_list)]
            else:
                env = [("input", test_case)]
            
            with capture_stdout() as stdout:
                lang_start = time.time()
                if bytecode and test.compile_to_bytecode:
                    # Bytecode execution
                    vm = BytecodeVM(bytecode)
                    vm.run(env=env)
                else:
                    # Interpreter execution - using the imported e function
                    try:
                        e(ast, env)
                    except Exception as inner_ex:
                        raise Exception(f"Error during execution: {type(inner_ex).__name__}: {str(inner_ex)}")
                lang_end = time.time()
            
            language_output = stdout.getvalue().strip()
            lang_time_ms = (lang_end - lang_start) * 1000
            
            # Compare outputs
            success = language_output == reference_output
            error_msg = None if success else f"Output mismatch: expected '{reference_output}', got '{language_output}'"
            
            return TestResult(
                success, language_output, reference_output, lang_time_ms, error_msg
            )
            
        except Exception as ex:
            return TestResult(
                False, "", reference_output, 0,
                f"Language execution failed: {type(ex).__name__}: {str(ex)}"
            )
    
    def log(self, message):
        """Log a message if verbose mode is enabled"""
        if self.verbose:
            print(message)
    
    def print_summary(self):
        """Print a summary of all tests that were run"""
        print("\n===== Reference Test Summary =====")
        
        total_tests = len(self.results)
        total_cases = sum(len(cases) for cases in self.results.values())
        passed_cases = sum(sum(1 for r in cases.values() if r.success) for cases in self.results.values())
        
        print(f"Tests: {total_tests}")
        
        if total_cases > 0:
            success_rate = (passed_cases / total_cases) * 100
            print(f"Test Cases: {passed_cases}/{total_cases} passed ({success_rate:.1f}%)")
        else:
            print("Test Cases: 0/0 passed (0.0%)")
        
        print("\nTest Results:")
        for test_name, cases in self.results.items():
            passed = sum(1 for r in cases.values() if r.success)
            total = len(cases)
            status = "✅ " if passed == total else "❌ "
            print(f"{status}{test_name}: {passed}/{total} cases passed")

# Example reference implementations
def fibonacci(n):
    """Reference implementation for Fibonacci sequence"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def sum_to_n(n):
    """Sum numbers from 1 to n"""
    return sum(range(1, n + 1))

def is_prime(n):
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def run_example_tests():
    """Run some example reference tests"""
    # Define test cases
    tests = [
        ReferenceTest(
            name="Fibonacci",
            description="Calculate the nth Fibonacci number",
            language_code="""
                fun fibonacci(n : int) : int {
                    if (n <= 1) {
                        return n;
                    }
                    int a = 0;
                    int b = 1;
                    int i = 2;
                    while (i <= n) {
                        int temp = b;
                        b = a + b;
                        a = temp;
                        i = i + 1;
                    }
                    return b;
                }
                println(fibonacci(input));
            """,
            reference_implementation=fibonacci,
            test_cases=[0, 1, 2, 5, 10, 15, 20]
        ),
        
        ReferenceTest(
            name="Sum to N",
            description="Calculate the sum of integers from 1 to n",
            language_code="""
                fun sumToN(n : int) : int {
                    int sum = 0;
                    int i = 1;
                    while (i <= n) {
                        sum = sum + i;
                        i = i + 1;
                    }
                    return sum;
                }
                println(sumToN(input));
            """,
            reference_implementation=sum_to_n,
            test_cases=[1, 5, 10, 100, 1000]
        ),
        
        ReferenceTest(
            name="Is Prime",
            description="Check if a number is prime",
            language_code="""
                fun isPrime(n : int) : int {
                    if (n <= 1) {
                        return 0;
                    }
                    if (n <= 3) {
                        return 1;
                    }
                    if (n % 2 == 0 or n % 3 == 0) {
                        return 0;
                    }
                    int i = 5;
                    while (i * i <= n) {
                        if (n % i == 0 or n % (i + 2) == 0) {
                            return 0;
                        }
                        i = i + 6;
                    }
                    return 1;
                }
                println(isPrime(input));
            """,
            reference_implementation=lambda n: 1 if is_prime(n) else 0,
            test_cases=[1, 2, 3, 4, 5, 13, 17, 20, 97, 100, 541]
        )
    ]
    
    # Run the tests
    runner = ReferenceTestRunner()
    for test in tests:
        runner.run_test(test)
    
    # Print summary
    runner.print_summary()

if __name__ == "__main__":
    run_example_tests()
