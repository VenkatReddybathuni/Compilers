# from tests.test_framework import TestCase, run_test_suite

# def run_tests():
#     test_cases = [
#         TestCase(
#             name="Project Euler #1 - Multiples of 3 or 5",
#             code="""
#             int x = 1;
#             int sum = 0;
#             while(x < 1000) {
#                 if (x % 3 == 0 or x % 5 == 0) {
#                     sum = sum + x;
#                 }
#                 x = x + 1;
#             }
#             println("Sum of all multiples of 3 or 5 below 1000: " ++ str(sum));
#             """,
#             expected_output="Sum of all multiples of 3 or 5 below 1000: 233168"
#         ),
#         TestCase(
#             name="Project Euler #2 - Even Fibonacci Sum",
#             code="""
#             int sum = 0;
#             int a = 1;
#             int b = 2;
#             while (b < 4000000) {
#                 if (b % 2 == 0) {
#                     sum = sum + b;
#                 }
#                 int temp = a + b;
#                 a = b;
#                 b = temp;
#             }
#             println("Sum of even-valued Fibonacci terms below 4 million: " ++ str(sum));
#             """,
#             expected_output="Sum of even-valued Fibonacci terms below 4 million: 4613732"
#         ),
#         TestCase(
#             name="Project Euler #3 - Largest Prime Factor",
#             code="""
#             int n = 600851475143;
#             int i = 2;
#             while (i * i <= n) {
#                 if (n % i == 0) {
#                     n = n / i;
#                 } else {
#                     i = i + 1;
#                 }
#             }
#             println("Largest prime factor of 600851475143: " ++ str(n));
#             """,
#             expected_output="Largest prime factor of 600851475143: 6857"
#         ),
#         # TestCase(
#         #     name="Project Euler #4 - Largest Palindrome Product",
#         #     code="""
#         #     int max = 0;
#         #     int i = 100;
#         #     while (i < 1000) {
#         #         int j = 100;
#         #         while (j < 1000) {
#         #             int product = i * j;
#         #             int number = product;
#         #             int reverse = 0;
#         #             while (number != 0) {
#         #                 reverse = reverse * 10 + number % 10;
#         #                 number = number / 10;
#         #             }
#         #             if (product == reverse and product > max) {
#         #                 max = product;
#         #             }
#         #             j = j + 1;
#         #         }
#         #         i = i + 1;
#         #     }
#         #     println("Largest palindrome product of two 3-digit numbers: " ++ str(max));
#         #     """,
#         #     expected_output="Largest palindrome product of two 3-digit numbers: 906609"
#         # ),
#         TestCase(
#             name="Project Euler #5 - Smallest Multiple",
#             code="""
#             int result = 1;
#             int i = 1;
#             while (i <= 20) {
#                 int a = result;
#                 int b = i;
#                 while (b != 0) {
#                     int temp = b;
#                     b = a % b;
#                     a = temp;
#                 }
#                 int gcd = a;
#                 result = (result * i) / gcd;
#                 i = i + 1;
#             }
#             println("Smallest number divisible by all numbers from 1 to 20: " ++ str(result));
#             """,
#             expected_output="Smallest number divisible by all numbers from 1 to 20: 232792560"
#         ),
#         TestCase(
#             name="Project Euler #6 - Sum Square Difference",
#             code="""
#             int sum = 0;
#             int sumsquares = 0;
#             int i = 1;
#             while (i <= 100) {
#                 sum = sum + i;
#                 sumsquares = sumsquares + (i * i);
#                 i = i + 1;
#             }
#             int squareofsum = sum * sum;
#             int difference = squareofsum - sumsquares;
#             println("Sum of squares = " ++ str(sumsquares));
#             println("Square of sum = " ++ str(squareofsum));
#             println("Difference = " ++ str(difference));
#             """,
#             expected_output="Sum of squares = 338350\nSquare of sum = 25502500\nDifference = 25164150"
#         ),
#         TestCase(
#             name="Project Euler #7 - 10001st Prime",
#             code="""
#             int count = 0;
#             int i = 2;
#             int result = 0;
#             while (count < 10001) {
#                 int j = 2;
#                 int prime = 1;
#                 while (j * j <= i) {
#                     if (i % j == 0) {
#                         prime = 0;
#                         break;
#                     }
#                     j = j + 1;
#                 }
#                 if (prime == 1) {
#                     count = count + 1;
#                     result = i;
#                 }
#                 i = i + 1;
#             }
#             println("10001st prime number: " ++ str(result));
#             """,
#             expected_output="10001st prime number: 104743"
#         ),
#         # TestCase(
#         #     name="Project Euler #8 - Largest Product in a Series",
#         #     code="""
#         #     string series = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450";
#         #     int max = 0;
#         #     int i = 0;
#         #     while (i < 987) {
#         #         int product = 1;
#         #         int j = 0;
#         #         while (j < 13) {
#         #             product = product * (series[i + j] - '0');
#         #             j = j + 1;
#         #         }
#         #         if (product > max) {
#         #             max = product;
#         #         }
#         #         i = i + 1;
#         #     }
#         #     println("Largest product of 13 adjacent digits: " ++ str(max));
#         #     """,
#         #     expected_output="Largest product of 13 adjacent digits: 23514624000"
#         # ),
#         # TestCase(
#         #     name="Project Euler #9 - Special Pythagorean Triplet",
#         #     code="""
#         #     int a = 1;
#         #     while (a < 1000) {
#         #         int b = a + 1;
#         #         while (b < 1000) {
#         #             int c = 1000 - a - b;
#         #             if (a * a + b * b == c * c) {
#         #                 println("Product of Pythagorean triplet: " ++ str(a * b * c));
#         #                 break;
#         #             }
#         #             b = b + 1;
#         #         }
#         #         a = a + 1;
#         #     }
#         #     """,
#         #     expected_output="Product of Pythagorean triplet: 31875000"
#         # ),
#         TestCase(
#             name="Project Euler #10 - Summation of Primes",
#             code="""
#             int n = 20000;
#             int i = 2;
#             int sum = 0;
#             while (i < n) {
#                 int j = 2;
#                 int prime = 1;
#                 while (j * j <= i) {
#                     if (i % j == 0) {
#                         prime = 0;
#                         break;
#                     }
#                     j = j + 1;
#                 }
#                 if (prime == 1) {
#                     sum = sum + i;
#                 }
#                 i = i + 1;
#             }
#             println("Sum of primes below 2 million: " ++ str(sum));
#             """,
#             expected_output="Sum of primes below 2 million: 142913828922"
#         ),

#     ]
    
#     results = run_test_suite(test_cases)
#     results.print_summary()

# if __name__ == "__main__":
#     run_tests()
