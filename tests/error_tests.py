from test_framework import TestCase, run_test_suite
from main import TypeError, ParseError


def run_tests():
    test_cases = [
         # Type Error Tests
        TestCase(
            name="Invalid Type in String Concat",
            code="""
            fun wrap(text : int) : string {
                return "[" ++ text ++ "]";
            }
            println(wrap("wrapped text"));
            """,
            expected_error=TypeError
        ),
        TestCase(
            name="Invalid Addition",
            code="""
            fun intadd(text : string) : int {
                return text + 2;
            }
            println(intadd("wrapped text"));
            """,
            expected_error=TypeError,
            # We don't check the specific error message, just that it's a TypeError
        ),
        TestCase(
            name="Out of Bounds Error",
            code="""
            int[] arr = [1, 2, 3];
            println(arr[3]);
            """,
            expected_error=IndexError
        ),

        # Array Type Error Tests
        TestCase(
            name="Array Type Mismatch - String in Int Array",
            code="""
            int[] nums = ["hello"];
            println(nums[0]);
            """,
            expected_error=TypeError
        ),
        TestCase(
            name="Array Assignment Type Mismatch",
            code="""
            int[] arr = [1, 2, 3];
            arr[1] = "string";
            """,
            expected_error=TypeError
        ),
        TestCase(
            name="Invalid Array Index Type",
            code="""
            int[] arr = [1, 2, 3];
            println(arr["1"]);
            """,
            expected_error=TypeError
        ),
        TestCase(
            name="Array Index Out of Bounds - Positive",
            code="""
            int[] arr = [1, 2, 3];
            println(arr[5]);
            """,
            expected_error=IndexError
        ),
        TestCase(
            name="Array Index Out of Bounds - Negative",
            code="""
            int[] arr = [1, 2, 3];
            println(arr[-1]);
            """,
            expected_error=IndexError
        ),
        TestCase(
            name="String Array Type Mismatch",
            code="""
            string[] words = [1, 2, 3];
            println(words[0]);
            """,
            expected_error=TypeError
        ),
        TestCase(
            name="String Array Assignment Type Mismatch",
            code="""
            string[] words = ["a", "b", "c"];
            words[1] = 42;
            """,
            expected_error=TypeError
        ),
        TestCase(
            name="Mixed Array Type in Function",
            code="""
            fun process(arr: int[]) : int {
                return len(arr);
            }
            string[] words = ["a", "b", "c"];
            println(process(words));
            """,
            expected_error=TypeError
        ),
    ]
    results = run_test_suite(test_cases)
    results.print_summary()


if __name__ == "__main__":
    run_tests()