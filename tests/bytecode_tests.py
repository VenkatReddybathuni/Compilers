from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from main import parse, BytecodeCompiler, BytecodeVM
from test_framework import capture_stdout 
from io import StringIO

def run_bytecode_test(code, expected_output=None, env=None):
    """Run a test through bytecode compilation and execution"""
    ast = parse(code)
    compiler = BytecodeCompiler()
    bytecode = compiler.compile(ast)
    
    # Print bytecode for inspection
    print("\nBytecode Instructions:")
    for i, instr in enumerate(bytecode['instructions']):
        args_str = ", ".join(map(str, instr.args)) if instr.args else ""
        print(f"{i}: {instr.opcode} {args_str}")
    
    print("\nConstants Pool:")
    for i, const in enumerate(bytecode['constants']):
        print(f"{i}: {repr(const)}")
    
    print("\nVariable Map:")
    for var, idx in bytecode['variables'].items():
        print(f"{var} -> {idx}")
    
    print(f"\nMax Stack Size: {bytecode['max_stack']}")
    
    # Run the bytecode
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
            assert False, f"Output mismatch: Line count differs"
        
        for i, (actual_line, expected_line) in enumerate(zip(actual_lines, expected_lines)):
            assert actual_line == expected_line, f"Line {i+1} mismatch:\nExpected: {expected_line}\nGot: {actual_line}"
        
        print("Output matches expected!")
    
    return bytecode

def test_arithmetic():
    print("\n===== Testing Arithmetic Operations =====")
    # Test each operation separately to isolate issues
    print("Testing addition and multiplication...")
    code1 = "println(2 + 3 * 4);"
    expected1 = "14"
    run_bytecode_test(code1, expected1)
    
    print("Testing subtraction...")
    code2 = "println(10 - 2);"
    expected2 = "8"
    run_bytecode_test(code2, expected2)
    
    print("Testing division...")
    code3 = "println(20 / 5);"
    expected3 = "4" 
    run_bytecode_test(code3, expected3)
    
    print("Testing modulo...")
    code4 = "println(7 % 3);"
    expected4 = "1"
    run_bytecode_test(code4, expected4)
    
    print("Testing power...")
    code5 = "println(2 ** 3);"
    expected5 = "8"
    run_bytecode_test(code5, expected5)

def test_variables():
    print("\n===== Testing Variables =====")
    code = """
    int x = 5;
    int y = 10;
    int z = x + y;
    println(z);
    """
    expected = "15"
    run_bytecode_test(code, expected)

def test_strings():
    print("\n===== Testing Strings =====")
    code = """
    string hello = "Hello";
    string world = "World";
    println(hello ++ " " ++ world);
    """
    expected = "Hello World"
    run_bytecode_test(code, expected)

def test_conditionals():
    print("\n===== Testing Conditionals =====")
    code = """
    int x = 10;
    if (x > 5) {
        println("Greater");
    } else {
        println("Less or Equal");
    }
    """
    expected = "Greater"
    run_bytecode_test(code, expected)

def test_loops():
    print("\n===== Testing Loops =====")
    code = """
    int sum = 0;
    int i = 1;
    while (i <= 5) {
        sum = sum + i;
        i = i + 1;
    }
    println(sum);
    """
    expected = "15"
    run_bytecode_test(code, expected)

def test_arrays():
    print("\n===== Testing Arrays =====")
    
    # Basic array creation and access
    print("Testing array creation and access...")
    code1 = """
    int[] numbers = [10, 20, 30, 40, 50];
    println(numbers[2]);
    """
    expected1 = "30"
    run_bytecode_test(code1, expected1)
    
    # Array assignment
    print("Testing array element assignment...")
    code2 = """
    int[] numbers = [10, 20, 30];
    numbers[1] = 99;
    println(numbers[1]);
    """
    expected2 = "99"
    run_bytecode_test(code2, expected2)
    
    # Array length
    # print("Testing array length...")
    # code3 = """
    # int[] numbers = [5, 10, 15, 20, 25];
    # println(len(numbers));
    # """
    # expected3 = "5"
    # run_bytecode_test(code3, expected3)
    
    # # Empty array
    # print("Testing empty array...")
    # code4 = """
    # int[] empty = [];
    # println(len(empty));
    # """
    # expected4 = "0"
    # run_bytecode_test(code4, expected4)
    
    # Array slicing
    print("Testing array slicing...")
    code5 = """
    int[] numbers = [10, 20, 30, 40, 50];
    int[] slice = numbers[1:4];
    println(slice[0]);
    println(slice[2]);
    """
    expected5 = "20\n40"
    run_bytecode_test(code5, expected5)
    
    # Array modification doesn't affect original
    print("Testing array independence after slicing...")
    code6 = """
    int[] original = [1, 2, 3, 4, 5];
    int[] slice = original[0:3];
    slice[0] = 99;
    println(slice[0]);
    println(original[0]);
    """
    expected6 = "99\n1"
    run_bytecode_test(code6, expected6)
    
    # Using arrays in calculations
    print("Testing array elements in calculations...")
    code7 = """
    int[] values = [5, 10, 15];
    int sum = values[0] + values[1] + values[2];
    println(sum);
    """
    expected7 = "30"
    run_bytecode_test(code7, expected7)
    
    # Array of strings
    print("Testing array of strings...")
    code8 = """
    string[] fruits = ["apple", "banana", "cherry"];
    println(fruits[0] ++ " and " ++ fruits[2]);
    """
    expected8 = "apple and cherry"
    run_bytecode_test(code8, expected8)

def test_functions():
    print("\n===== Testing Functions =====")
    
    # Basic function definition and call
    print("Testing basic function call...")
    code1 = """
    fun add(a: int): int {
        return a + 5;
    }
    println(add(10));
    """
    expected1 = "15"
    run_bytecode_test(code1, expected1)
    
    # Function with multiple statements
    print("Testing function with multiple statements...")
    code2 = """
    fun calculate(x: int): int {
        int y = x * 2;
        int z = y + 10;
        return z / 2;
    }
    println(calculate(5));
    """
    expected2 = "10"
    run_bytecode_test(code2, expected2)
    
    # Function with conditional logic
    print("Testing function with conditionals...")
    code3 = """
    fun max(a: int): int {
        if (a > 10) {
            return a;
        } else {
            return 10;
        }
    }
    println(max(5));
    println(max(15));
    """
    expected3 = "10\n15"
    run_bytecode_test(code3, expected3)
    
    # Recursive function
    print("Testing recursive function...")
    code4 = """
    fun factorial(n: int): int {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    println(factorial(5));
    """
    expected4 = "120"
    run_bytecode_test(code4, expected4)
    
    # # Function working with arrays
    # print("Testing function with arrays...")
    # code5 = """
    # fun sumArray(arr: int[]): int {
    #     int sum = 0;
    #     int i = 0;
    #     while (i < len(arr)) {
    #         sum = sum + arr[i];
    #         i = i + 1;
    #     }
    #     return sum;
    # }
    # int[] numbers = [10, 20, 30, 40];
    # println(sumArray(numbers));
    # """
    # expected5 = "100"
    # run_bytecode_test(code5, expected5)
    
    # Function with string manipulation
    print("Testing function with strings...")
    code6 = """
    fun greet(name: string): string {
        return "Hello, " ++ name ++ "!";
    }
    println(greet("World"));
    """
    expected6 = "Hello, World!"
    run_bytecode_test(code6, expected6)

# Update the run_tests function to include the new test function
def run_tests():
    try:
        test_arithmetic()
        test_variables()
        test_strings()
        test_conditionals()
        test_loops()
        test_arrays()
        test_functions()  # Add the new test function
        print("\nAll bytecode compilation tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    run_tests()
