from test_framework import TestCase, run_test_suite
from main import TypeError, ParseError

def run_tests():
    test_cases = [
        # Basic Operation Tests with environment
        TestCase(
            name="If with Environment Variables",
            code='if (x >= 10 and y <= 20) { println(x + y); } else { println(x - y); };',
            expected_output="25",
            env=[("x", 15), ("y", 10)]
        ),
        TestCase(
            name="Power Operation",
            code='println(2 ** 3);',
            expected_output="8"
        ),
        TestCase(
            name="Modulo Operation",
            code='println(17 % 5);',
            expected_output="2"
        ),
        TestCase(
            name="Complex Arithmetic 1",
            code='println((2 + 3) * 4);',
            expected_output="20"
        ),
        TestCase(
            name="Complex Arithmetic 2",
            code='println((2 + 3) * (4 + 5));',
            expected_output="45"
        ),

        # String Operations
        TestCase(
            name="String Concatenation",
            code='println("Hello" ++ " World");',
            expected_output="Hello World"
        ),

        # Control Flow Tests
        TestCase(
            name="If-Else with Environment",
            code="""
            if ((x == 15) and y < 20) { 
                println((x + y)*y); 
            } else { 
                println(x - y); 
            };
            """,
            expected_output="250",
            env=[("x", 15), ("y", 10)]
        ),

        # Let Expression Tests
        TestCase(
            name="Simple Let Expression",
            code="""
            int a = 3;
            int b = a + 2;
            println(a + b);
            """,
            expected_output="8"
        ),
        TestCase(
            name="Let with Multiplication",
            code="""
            int x = 5;
            int y = x * 2;
            println(x + y);
            """,
            expected_output="15"
        ),

        # Function Tests
        TestCase(
            name="Simple Function",
            code="""
            fun double(x : int) : int {
                return x + x;
            }
            println(double(5));
            """,
            expected_output="10"
        ),
        TestCase(
            name="String Function",
            code="""
            fun greet(name : string) : string {
                return "Hello " ++ name ++ "!";
            }
            println(greet("World"));
            """,
            expected_output="Hello World!"
        ),

        # String Operation Tests
        TestCase(
            name="Error Code Function",
            code="""
            fun error(code : int) : string {
                if (code > 0) {
                    return "Error Code: " ++ str(code);
                } else {
                    return "No Error";
                }
            }
            println(error(404));
            """,
            expected_output="Error Code: 404"
        ),

        # While Loop Tests
        TestCase(
            name="Simple Counter",
            code="""
            int x = 0;
            while (x < 5) {
                x = x + 1;
                println(x);
            }
            """,
            expected_output="1\n2\n3\n4\n5"
        ),
        TestCase(
            name="Sum Calculator",
            code="""
            int sum = 0;
            int i = 1;
            while (i <= 10) {
                sum = sum + i;
                i = i + 1;
            }
            println(sum);
            """,
            expected_output="55"
        ),

        # Break and Continue Tests
        TestCase(
            name="Continue Statement",
            code="""
            int x = 0;
            while (x < 5) {
                x = x + 1;
                if (x == 3) {
                    continue;
                }
                println(x);
            }
            """,
            expected_output="1\n2\n4\n5"
        ),
        TestCase(
            name="Break Statement",
            code="""
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
            """,
            expected_output="10"
        ),

        # Project Euler Test
        TestCase(
            name="Even Fibonacci Sum",
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
            println(sum);
            """,
            expected_output="4613732"
        ),

        # Function Assignment Tests
        TestCase(
            name="Function with Variable Assignment",
            code="""
            fun square(x : int) : int {
                return x * x;
            }
            int result = square(5);
            println("Square of 5: " ++ str(result));
            """,
            expected_output="Square of 5: 25"
        ),
        TestCase(
            name="Equality Comparison",
            code='println(x == y);',
            expected_output="False",
            env=[("x", 15), ("y", 10)]
        ),
        TestCase(
            name="Inequality Comparison",
            code='println(x != y);',
            expected_output="True",
            env=[("x", 15), ("y", 10)]
        ),
        TestCase(
            name="Power Plus Operation",
            code='println((2 ** 3) + 1);',
            expected_output="9"
        ),
        TestCase(
            name="Word Repeat Function",
            code="""
            fun repeat(word : string) : string {
                return word ++ " " ++ word;
            }
            println(repeat("hello"));
            """,
            expected_output="hello hello"
        ),
        TestCase(
            name="Multiplication Table",
            code="""
            int i = 1;
            while (i <= 10) {
                println("17*" ++ str(i) ++ " = " ++ str(17 * i));
                i = i + 1;
            }
            """,
            expected_output="17*1 = 17\n17*2 = 34\n17*3 = 51\n17*4 = 68\n17*5 = 85\n17*6 = 102\n17*7 = 119\n17*8 = 136\n17*9 = 153\n17*10 = 170"
        ),
        TestCase(
            name="Add One with Variables",
            code="""
            fun addOne(x : int) : int {
                return x + 1;
            }
            int a = 5;
            int b = addOne(a);
            println("a: " ++ str(a) ++ ", b: " ++ str(b));
            """,
            expected_output="a: 5, b: 6"
        ),
        TestCase(
            name="Chain of Doubles",
            code="""
            fun double(x : int) : int {
                return x + x;
            }
            int x = 10;
            int y = double(x);
            int z = double(y);
            println("x: " ++ str(x) ++ ", y: " ++ str(y) ++ ", z: " ++ str(z));
            """,
            expected_output="x: 10, y: 20, z: 40"
        ),
        # Array Creation and Access Tests
        TestCase(
            name="Array Creation and Access",
            code="""
            int[] arr = [1, 2, 3, 4, 5];
            println(arr[0]);
            println(arr[4]);
            """,
            expected_output="1\n5"
        ),
        TestCase(
            name="Array Assignment",
            code="""
            int[] arr = [1, 2, 3];
            arr[1] = 10;
            println(arr[1]);
            """,
            expected_output="10"
        ),
        TestCase(
            name="Array in Expressions",
            code="""
            int[] arr = [1, 2, 3];
            println(arr[0] + arr[1] + arr[2]);
            """,
            expected_output="6"
        ),
        TestCase(
            name="String Indexing",
            code="""
            string st = "Hello";
            println(st[0]);
            println(st[4]);
            """,
            expected_output="H\no"
        ),
        TestCase(
            name="Array Length",
            code="""
            int[] arr = [1, 2, 3, 4, 5];
            println(len(arr));
            """,
            expected_output="5"
        ),
        TestCase(
            name="String Length",
            code="""
            string st = "Hello";
            println(len(st));
            """,
            expected_output="5"
        ),
        TestCase(
            name="Array in Function",
            code="""
            fun sumArray(arr: int[]) : int {
                int sum = 0;
                int i = 0;
                while(i < len(arr)) {
                    sum = sum + arr[i];
                    i = i + 1;
                }
                return sum;
            }
            int[] numbers = [1, 2, 3, 4, 5];
            println(sumArray(numbers));
            """,
            expected_output="15"
        ),
        TestCase(
            name="Nested Array Operations",
            code="""
            int[] arr = [10, 20, 30];
            arr[1] = arr[0] + arr[2];
            println(arr[1]);
            """,
            expected_output="40"
        ),

        # String Array Tests
        TestCase(
            name="String Array Creation and Access",
            code="""
            string[] words = ["hello", "world", "!"];
            println(words[0] ++ words[1] ++ words[2]);
            """,
            expected_output="helloworld!"
        ),
        TestCase(
            name="String Array Assignment",
            code="""
            string[] greetings = ["hi", "hello", "hey"];
            greetings[1] = "HELLO";
            println(greetings[1]);
            """,
            expected_output="HELLO"
        ),
        TestCase(
            name="String Array in Function",
            code="""
            fun joinWords(words: string[]) : string {
                string result = "";
                int i = 0;
                while(i < len(words)) {
                    result = result ++ words[i];
                    i = i + 1;
                }
                return result;
            }
            string[] arr = ["a", "b", "c"];
            println(joinWords(arr));
            """,
            expected_output="abc"
        ),
        TestCase(
            name="Mixed Array Operations",
            code="""
            string[] words = ["count:", "sum:"];
            int[] nums = [1, 2, 3];
            println(words[0] ++ str(len(nums)));
            println(words[1] ++ str(nums[0] + nums[1] + nums[2]));
            """,
            expected_output="count:3\nsum:6"
        ),
        TestCase(
            name="Array Slicing",
            code="""
            int[] arr = [1, 2, 3, 4, 5];
            int[] sliced = arr[1:4];
            println(sliced[0]);
            println(sliced[1]);
            println(sliced[2]);
            """,
            expected_output="2\n3\n4"
        ),
        TestCase(
            name="String Slicing",
            code="""
            string s = "hello world";
            string sliced = s[1:5];
            println(sliced);
            """,
            expected_output="ello"
        ),
         TestCase(
            name="Dictionary Creation and Access",
            code="""
            dict d = {"name": "Alice", "age": 30, "city": "Wonderland"};
            string name = d{"name"};
            int age = d{"age"};
            string city = d{"city"};
            println(name);
            println(age);
            println(city);
            """,
            expected_output="Alice\n30\nWonderland"
        ),
        TestCase(
            name="Dictionary Assignment",
            code="""
            dict d = {"a": 1, "b": 2};
            d{"a"} = 10;
            d{"b"} = 20;
            int a = d{"a"};
            int b = d{"b"};
            println(a);
            println(b);
            """,
            expected_output="10\n20"
        ),
        TestCase(
            name="Dictionary Update and Access",
            code="""
            dict d = {"x": 5, "y": 10};
            d{"x"} = d{"x"} + d{"y"};
            int result = d{"x"};
            println(result);
            """,
            expected_output="15"
        ),
    ]

    # Run all tests and print summary
    results = run_test_suite(test_cases)
    results.print_summary()

if __name__ == "__main__":
    run_tests()