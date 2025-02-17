from main import e, parse

def run_test_cases(tests, env=None):
    i = 0
    for test in tests:
        i = i+1
        try:
            # print(f"\nTest: {test}")
            print(f"Project Euler Test #:{i}")
            e(parse(test), env)
            print("-" * 30)
        except Exception as err:
            print(f"Error in test: {err}")
            print("-" * 30)



def run_tests():
    project_euler_tests = [
        ### Project Euler #1 - Multiples of 3 or 5
        """
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
        ### Project Euler #2 - Even Fibonacci Sum
        """
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
        ### Project Euler #3 - Largest Prime Factor
        """
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
        ### Project Euler #4 - Largest Palindrome Product
        """
        println("Need to add string indexing to the language to solve this problem.");
        """,
        ### Project Euler #5 - Smallest Multiple
        """
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
        ### Project Euler #6 - Sum Square Difference
        """
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
        """
    ]    
    run_test_cases(project_euler_tests)



if __name__ == "__main__":
    run_tests()
