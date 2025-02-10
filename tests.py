from main import e, parse

def run_tests():
    # Basic operation test cases
    test_cases = [
        'if (x >= 10 and y <= 20) { x + y } else { x - y }',
        '2 ** 3',  # Power operation
        '17 % 5',  # Modulo operation
        '"Hello" ++ " World"',  # String concatenation
        'x == y',  # Equality comparison
        'x != y',  # Inequality comparison
        '(2 + 3) * 4',  # Should evaluate to 20
        '2 + (3 * 4)',  # Should evaluate to 14
        'if (x > 10) { x + y } else { x - y }',
        '(2 ** 3) + 1',  # Should evaluate to 9
        '((2 + 3) * (4 + 5))',  # Should evaluate to 45
    ]

    # Run basic test cases
    test_env = [("x", 15), ("y", 10)]
    print("\nRunning basic test cases:")
    run_test_cases(test_cases, test_env)

    # Test if conditions
    print("\nTesting if conditions:")
    if_tests = [
        'if ((x == 15) and y < 20) { (x + y)*y } else { x - y }',
        'if (x > 10) { x + y } else { x - y }',
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
        double(5);
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
