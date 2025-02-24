from test_framework import TestCase, run_test_suite

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
    ]
    
    results = run_test_suite(test_cases)
    results.print_summary()

if __name__ == "__main__":
    run_tests()
