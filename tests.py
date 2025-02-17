from main import e, parse

def run_tests():
    # Basic operation test cases
    test_cases = [
        'if (x >= 10 and y <= 20) { println(x + y); } else { println(x - y); };',
        'println(2 ** 3);',  # Power operation
        'println(17 % 5);',  # Modulo operation
        'println("Hello" ++ " World");',  # String concatenation
        'println(x == y);',  # Equality comparison
        'println(x != y);',  # Inequality comparison
        'println((2 + 3) * 4);',  # Should evaluate to 20
        'println(2 + (3 * 4));',  # Should evaluate to 14
        'if (x > 10) { println(x + y); } else { println(x - y); };',
        'println((2 ** 3) + 1);',  # Should evaluate to 9
        'println((2 + 3) * (4 + 5));',  # Should evaluate to 45
    ]

    # Run basic test cases
    test_env = [("x", 15), ("y", 10)]
    print("\nRunning basic test cases:")
    run_test_cases(test_cases, test_env)

    # Test if conditions
    print("\nTesting if conditions:")
    if_tests = [
        'if ((x == 15) and y < 20) { println((x + y)*y); } else { println(x - y); };',
        'if (x > 10) { println(x + y); } else { println(x - y); };',
    ]
    run_test_cases(if_tests, test_env)

    # Test let expressions
    print("\nTesting let expressions:")
    let_tests = [
        """
        int a = 3;
        int b = a + 2;
        println(a + b);
        """,
        """
        int x = 5;
        int y = x * 2;
        println(x + y);
        """
    ]
    run_test_cases(let_tests)

    # Test functions
    print("\nTesting functions:")
    function_tests = [
        """
        fun double(x : int) : int {
            return x + x;
        }
        println(double(5));
        """,
        """
        fun greet(name : string) : string {
            return "Hello " ++ name ++ "!";
        }
        println(greet("World"));
        """
    ]
    run_test_cases(function_tests)

    # Test string operations
    print("\nTesting string operations:")
    string_tests = [
        """
        fun error(code : int) : string {
            if (code > 0) {
                return "Error Code: " ++ str(code);
            } else {
                return "No Error";
            }
        }
        println(error(404));
        """,
        """
        fun repeat(word : string) : string {
            return word ++ " " ++ word;
        }
        println(repeat("hello"));
        """
    ]
    run_test_cases(string_tests)

    # Test type errors
    print("\nTesting type errors:")
    error_tests = [
        
        """
        fun wrap(text : int) : string {
            return "[" ++ text ++ "]";
        }
        println(wrap("wrapped text"));
        """,
        """
        fun intadd(text : string) : int {
            return 2 + text;
        }
        println(intadd("wrapped text"));
        """,
        """
        fun compare(x : int) : bool {
            return x + true;
        }
        compare(5);
        """,
        # This should fail: non-boolean condition in if statement
        """
        fun conditional(x : string) : int {
            if (x == "test") { return 1; } else { return 0; }
        }
        int num = conditional("test");
        println(num);
        """,
        # Additional test to ensure boolean conditions work
        """
        fun validConditional(x : int) : int {
            if (x > 0) { return 1; } else { return 0; }
        }
        println(validConditional(5));
        """,
        """
        fun wrongReturn(x : int) : string {
            return x;
        }
        println(wrongReturn(42));
        """,
        """
        fun mixedMath(x : int) : int {
            return x * "2";
        }
        println(mixedMath(10));
        """
    ]
    run_test_cases(error_tests)

    # Test while loops
    print("\nTesting while loops:")
    while_tests = [
        """
        int x = 0;
        while (x < 5) {
            x = x + 1;
            println(x);
        }
        """,
        """
        int sum = 0;
        int i = 1;
        while (i <= 10) {
            sum = sum + i;
            i = i + 1;
        }
        println(sum);
        """
    ]
    run_test_cases(while_tests)

    # Test while loops with continue and break
    print("\nTesting while loops with continue and break:")
    while_control_tests = [
        """
        int x = 0;
        while (x < 5) {
            x = x + 1;
            if (x == 3) {
                continue;
            }
            println(x);
        }
        """,
        """
        int sum = 0;
        int i = 1;
        while (i <= 10) {
            if (i == 5) {
                break;
            }
            sum = sum + i;
            i = i + 1;
        }
        println(sum);
        """
    ]
    run_test_cases(while_control_tests)

    # Test Project Euler - Even Fibonacci Sum
    print("\nTesting Project Euler - Even Fibonacci Sum:")
    euler_tests = [
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
        println(sum);  
        """
    ]
    run_test_cases(euler_tests)

    # Test multiplication table
    print("\nTesting 17 times table:")
    multiplication_table = [
        """
        int i = 1;
        while (i <= 10) {
            println("17*" ++ str(i) ++ " = " ++ str(17 * i));
            i = i + 1;
        }
        """
    ]
    run_test_cases(multiplication_table)

    # Test function calls with variable assignments
    print("\nTesting function calls with variable assignments:")
    function_assignment_tests = [
        """
        fun square(x : int) : int {
            return x * x;
        }
        int result = square(5);
        println("Square of 5: " ++ str(result));
        """,
        """
        fun addOne(x : int) : int {
            return x + 1;
        }
        int a = 5;
        int b = addOne(a);
        println("a: " ++ str(a) ++ ", b: " ++ str(b));
        """,
        """
        fun makeGreeting(name : string) : string {
            return "Hello " ++ name;
        }
        string msg = makeGreeting("Alice");
        println(msg);
        """,
        """
        fun double(x : int) : int {
            return x + x;
        }
        int x = 10;
        int y = double(x);
        int z = double(y);
        println("x: " ++ str(x) ++ ", y: " ++ str(y) ++ ", z: " ++ str(z));
        """
    ]
    run_test_cases(function_assignment_tests)

def run_test_cases(tests, env=None):
    for test in tests:
        try:
            print(f"\nTest: {test}")
            e(parse(test), env)
            print("-" * 30)
        except Exception as err:
            print(f"Error in test: {err}")
            print("-" * 30)

if __name__ == "__main__":
    run_tests()
