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
    ]
    results = run_test_suite(test_cases)
    results.print_summary()


if __name__ == "__main__":
    run_tests()    