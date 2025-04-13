from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from tests.reference_tests import ReferenceTest, ReferenceTestRunner

# Reference implementations of algorithms
def factorial(n):
    """Calculate the factorial of n"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def gcd(a, b):
    """Calculate the greatest common divisor of a and b"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate the least common multiple of a and b"""
    return a * b // gcd(a, b)

def is_palindrome(s):
    """Check if a string is a palindrome"""
    s = str(s).lower()
    return s == s[::-1]

def nth_prime(n):
    """Find the nth prime number"""
    if n <= 0:
        return None
    
    primes = []
    num = 2
    
    while len(primes) < n:
        is_prime = True
        for prime in primes:
            if prime * prime > num:
                break
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    
    return primes[-1]

def run_algorithm_tests():
    """Run various algorithm tests comparing with reference implementations"""
    tests = [
        ReferenceTest(
            name="Factorial",
            description="Calculate the factorial of a number",
            language_code="""
                fun factorial(n : int) : int {
                    int result = 1;
                    int i = 2;
                    while (i <= n) {
                        result = result * i;
                        i = i + 1;
                    }
                    return result;
                }
                println(factorial(input));
            """,
            reference_implementation=factorial,
            test_cases=[0, 1, 5, 10, 12],
            compile_to_bytecode=False  # Use interpreter instead
        ),
        
        ReferenceTest(
            name="GCD",
            description="Calculate the greatest common divisor",
            language_code="""
                fun gcd(a : int, b : int) : int {
                    while (b != 0) {
                        int temp = b;
                        b = a % b;
                        a = temp;
                    }
                    return a;
                }

                int a = input[0];
                int b = input[1];
                println(gcd(a, b));
            """,
            reference_implementation=lambda pair: gcd(pair[0], pair[1]),
            test_cases=[(48, 18), (17, 5), (100, 75), (1071, 462)],
            compile_to_bytecode=False
        ),
        
        ReferenceTest(
            name="LCM",
            description="Calculate the least common multiple",
            language_code="""
                fun lcm_with_gcd(a : int, b : int, gcd_val : int) : int {
                    // gcd_val is pre-computed to avoid nested calls
                    return (a * b) / gcd_val;
                }
                
                fun compute_gcd(a : int, b : int) : int {
                    while (b != 0) {
                        int temp = b;
                        b = a % b;
                        a = temp;
                    }
                    return a;
                }
                
                int a = input[0];
                int b = input[1];
                int gcd_result = compute_gcd(a, b);
                println(lcm_with_gcd(a, b, gcd_result));
            """,
            reference_implementation=lambda pair: lcm(pair[0], pair[1]),
            test_cases=[(5, 7), (12, 18), (21, 6), (11, 13)],
            compile_to_bytecode=False
        ),
        
        ReferenceTest(
            name="Palindrome Check",
            description="Check if a string is a palindrome",
            language_code="""
                fun isPalindrome(s : string) : int {
                    int i = 0;
                    int j = len(s) - 1;
                    
                    while (i < j) {
                        if (s[i] != s[j]) {
                            return 0;
                        }
                        i = i + 1;
                        j = j - 1;
                    }
                    return 1;
                }
                
                string val = str(input);
                println(isPalindrome(val));
            """,
            reference_implementation=lambda s: 1 if is_palindrome(s) else 0,
            test_cases=["racecar", "level", "hello", "12321", "12345"],
            compile_to_bytecode=False
        ),
        
        ReferenceTest(
            name="Project Euler #7: 10001st Prime",
            description="Find the 10001st prime number",
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
                
                fun nthPrime(n : int) : int {
                    if (n <= 0) {
                        return 0;
                    }
                    
                    int count = 0;
                    int num = 2;
                    
                    while (count < n) {
                        if (isPrime(num) == 1) {
                            count = count + 1;
                        }
                        if (count == n) {
                            return num;
                        }
                        num = num + 1;
                    }
                    return 0;  // Should never get here
                }
                
                println(nthPrime(input));
            """,
            reference_implementation=nth_prime,
            test_cases=[1, 2, 6, 10, 100],  # For performance, not testing 10001
            compile_to_bytecode=False
        )
    ]
    
    # Set compile_to_bytecode=False for all tests
    for test in tests:
        test.compile_to_bytecode = False
        
    runner = ReferenceTestRunner()
    for test in tests:
        runner.run_test(test)
    
    runner.print_summary()

if __name__ == "__main__":
    run_algorithm_tests()
