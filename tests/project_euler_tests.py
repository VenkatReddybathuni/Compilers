from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from test_framework import TestCase, capture_stdout
from main import parse, BytecodeCompiler, BytecodeVM

def run_bytecode_euler_test(code, expected_output=None):
    """Run a Project Euler problem using the bytecode VM"""
    print("\nCompiling code...")
    ast = parse(code)
    compiler = BytecodeCompiler()
    bytecode = compiler.compile(ast)
    
    # Print bytecode statistics
    print(f"\nBytecode Stats:")
    print(f"Instructions: {len(bytecode['instructions'])}")
    print(f"Constants: {len(bytecode['constants'])}")
    print(f"Variables: {len(bytecode['variables'])}")
    print(f"Max Stack Size: {bytecode['max_stack']}")
    
    # Run the bytecode
    print("\nExecuting bytecode...")
    with capture_stdout() as stdout:
        vm = BytecodeVM(bytecode)
        vm.run()
    
    actual_output = stdout.getvalue().strip()
    
    if expected_output is not None:
        expected = expected_output.strip()
        print(f"\nExpected output: {expected}")
        print(f"Actual output: {actual_output}")
        
        # Compare outputs, handling newlines properly
        actual_lines = actual_output.split('\n')
        expected_lines = expected.split('\n')
        
        if len(actual_lines) != len(expected_lines):
            print(f"ERROR: Line count mismatch. Expected {len(expected_lines)} lines, got {len(actual_lines)} lines")
            return False
        
        for i, (actual_line, expected_line) in enumerate(zip(actual_lines, expected_lines)):
            if actual_line != expected_line:
                print(f"ERROR: Line {i+1} mismatch:\nExpected: {expected_line}\nGot: {actual_line}")
                return False
        
        print("Output matches expected!")
        return True
    
    return None

def run_tests():
    test_cases = [
        TestCase(
            name="Project Euler #1 - Multiples of 3 or 5",
            code="""
            int x = 1;
            int sum = 0;
            while(x < 1000) {
                if (x % 3 == 0 or x % 5 == 0) {
                    sum = sum + x;
                }
                x = x + 1;
            }
            println("Sum of all multiples of 3 or 5 below 1000: " ++ str(sum));
            """,
            expected_output="Sum of all multiples of 3 or 5 below 1000: 233168"
        ),
        TestCase(
            name="Project Euler #2 - Even Fibonacci Sum",
            code="""
            int sum = 0;
            int a = 1;
            int b = 2;
            while (b < 4000000) {
                if (b % 2 == 0) {
                    sum = sum + b;
                }
                int temp = a + b;
                a = b;
                b = temp;
            }
            println("Sum of even-valued Fibonacci terms below 4 million: " ++ str(sum));
            """,
            expected_output="Sum of even-valued Fibonacci terms below 4 million: 4613732"
        ),
        TestCase(
            name="Project Euler #3 - Largest Prime Factor",
            code="""
            int n = 600851475143;
            int i = 2;
            while (i * i <= n) {
                if (n % i == 0) {
                    n = n / i;
                } else {
                    i = i + 1;
                }
            }
            println("Largest prime factor of 600851475143: " ++ str(n));
            """,
            expected_output="Largest prime factor of 600851475143: 6857"
        ),
        TestCase(
            name="Project Euler #4 - Largest Palindrome Product (Optimized)",
            code="""
            
            int maxpalindrome = 0;
            int i = 99;  

            while (i >= 10) {
                int j = 99;  
                while (j >= i) {  
                    int product = i * j;
                    
                    
                    if (product <= maxpalindrome) {
                        break;
                    }
                    
                    int reversed = 0;
                    int temp = product;
                    while (temp > 0) {
                        reversed = reversed * 10 + temp % 10;
                        temp = temp / 10;
                    }
                    
                    if (product == reversed and product > maxpalindrome) {
                        maxpalindrome = product;
                    }
                    j = j - 1;
                }
                i = i - 1;
            }

            println("Largest palindrome made from the product of two 2-digit numbers: " ++ str(maxpalindrome));
            """,
            expected_output="Largest palindrome made from the product of two 2-digit numbers: 9009"
        ),
        TestCase(
            name="Project Euler #5 - Smallest Multiple",
            code="""
            int result = 1;
            int i = 1;
            while (i <= 20) {
                int a = result;
                int b = i;
                while (b != 0) {
                    int temp = b;
                    b = a % b;
                    a = temp;
                }
                int gcd = a;
                result = (result * i) / gcd;
                i = i + 1;
            }
            println("Smallest number divisible by all numbers from 1 to 20: " ++ str(result));
            """,
            expected_output="Smallest number divisible by all numbers from 1 to 20: 232792560"
        ),
        TestCase(
            name="Project Euler #6 - Sum Square Difference",
            code="""
            int sum = 0;
            int sumsquares = 0;
            int i = 1;
            while (i <= 100) {
                sum = sum + i;
                sumsquares = sumsquares + (i * i);
                i = i + 1;
            }
            int squareofsum = sum * sum;
            int difference = squareofsum - sumsquares;
            println("Sum of squares = " ++ str(sumsquares));
            println("Square of sum = " ++ str(squareofsum));
            println("Difference = " ++ str(difference));
            """,
            expected_output="Sum of squares = 338350\nSquare of sum = 25502500\nDifference = 25164150"
        ),
        TestCase(
            name="Project Euler #7 - 10001st Prime",
            code="""
            int count = 0;
            int i = 2;
            int result = 0;
            while (count < 10001) {
                int j = 2;
                int prime = 1;
                while (j * j <= i) {
                    if (i % j == 0) {
                        prime = 0;
                        break;
                    }
                    j = j + 1;
                }
                if (prime == 1) {
                    count = count + 1;
                    result = i;
                }
                i = i + 1;
            }
            println("10001st prime number: " ++ str(result));
            """,
            expected_output="10001st prime number: 104743"
        ),
        TestCase(
            name="Project Euler #10 - Summation of Primes (with smaller limit)",
            code="""
            int n = 20000; 
            int i = 2;
            int sum = 0;
            while (i < n) {
                int j = 2;
                int prime = 1;
                while (j * j <= i) {
                    if (i % j == 0) {
                        prime = 0;
                        break;
                    }
                    j = j + 1;
                }
                if (prime == 1) {
                    sum = sum + i;
                }
                i = i + 1;
            }
            println("Sum of primes below 20,000: " ++ str(sum));
            """,
            expected_output="Sum of primes below 20,000: 21171191"
        ),
    ]
    
    # Use the bytecode VM for execution instead of normal run_test_suite
    print("\n=== Running Project Euler Problems with Bytecode VM ===")
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        print(f"\n--- Running {test_case.name} ---")
        
        try:
            result = run_bytecode_euler_test(test_case.code, test_case.expected_output)
            if result:
                passed += 1
                print(f"✅ Test passed: {test_case.name}")
            else:
                failed += 1
                print(f"❌ Test failed: {test_case.name}")
        except Exception as e:
            failed += 1
            import traceback
            print(f"❌ Exception in {test_case.name}: {type(e).__name__}: {e}")
            traceback.print_exc()
    
    print(f"\n=== Project Euler Bytecode Tests Summary: {passed} passed, {failed} failed ===")

if __name__ == "__main__":
    run_tests()
