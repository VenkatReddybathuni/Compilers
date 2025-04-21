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
    print("Testing array length...")
    code3 = """
    int[] numbers = [5, 10, 15, 20, 25];
    println(len(numbers));
    """
    expected3 = "5"
    run_bytecode_test(code3, expected3)
    
    # Empty array
    print("Testing empty array...")
    code4 = """
    int[] empty = [];
    println(len(empty));
    """
    expected4 = "0"
    run_bytecode_test(code4, expected4)
    
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
    
    # Nested array operations
    print("Testing nested array indexing...")
    code9 = """
    int[] nums = [10, 20, 30, 40, 50];
    println(nums[nums[0] / 5]);
    """
    expected9 = "30"
    run_bytecode_test(code9, expected9)
    
    # Array operations in loops
    print("Testing array operations in loops...")
    code10 = """
    int[] arr = [1, 2, 3, 4, 5];
    int i = 0;
    int sum = 0;
    while (i < len(arr)) {
        sum = sum + arr[i];
        i = i + 1;
    }
    println(sum);
    """
    expected10 = "15"
    run_bytecode_test(code10, expected10)
    
    # Array element assignment in loops
    print("Testing array assignment in loops...")
    code11 = """
    int[] arr = [0, 0, 0, 0, 0];
    int i = 0;
    while (i < len(arr)) {
        arr[i] = i * 10;
        i = i + 1;
    }
    i = 0;
    while (i < len(arr)) {
        println(arr[i]);
        i = i + 1;
    }
    """
    expected11 = "0\n10\n20\n30\n40"
    run_bytecode_test(code11, expected11)
    
    # Array with calculated indices
    print("Testing array with calculated indices...")
    code12 = """
    int[] values = [5, 10, 15, 20, 25];
    int a = 1;
    int b = 3;
    println(values[a + b]);
    """
    expected12 = "25"
    run_bytecode_test(code12, expected12)

def test_dictionaries():
    print("\n===== Testing Dictionaries =====")
    
    # Basic dictionary creation and access
    print("Testing dictionary creation and access...")
    code1 = """
    dict scores = {
        "Alice": 95,
        "Bob": 87,
        "Charlie": 92
    };
    println(scores{"Alice"});
    """
    expected1 = "95"
    run_bytecode_test(code1, expected1)
    
    # Dictionary assignment
    print("Testing dictionary element assignment...")
    code2 = """
    dict data = {"x": 10, "y": 20};
    data{"x"} = 99;
    println(data{"x"});
    """
    expected2 = "99"
    run_bytecode_test(code2, expected2)
    
    # Adding new key to dictionary
    print("Testing adding new key to dictionary...")
    code3 = """
    dict items = {"first": 1, "second": 2};
    items{"third"} = 3;
    println(items{"third"});
    """
    expected3 = "3"
    run_bytecode_test(code3, expected3)
    
    # Using dictionary values in calculations
    print("Testing dictionary values in calculations...")
    code4 = """
    dict prices = {"apple": 5, "banana": 3, "orange": 4};
    int total = prices{"apple"} + prices{"orange"};
    println(total);
    """
    expected4 = "9"
    run_bytecode_test(code4, expected4)
    
    # String keys from variables
    print("Testing dictionary access with variable keys...")
    code5 = """
    dict inventory = {"sword": 10, "shield": 5, "potion": 20};
    string item = "shield";
    println(inventory{item});
    """
    expected5 = "5"
    run_bytecode_test(code5, expected5)
    
    # Dictionary with string values
    print("Testing dictionary with string values...")
    code6 = """
    dict translations = {"hello": "hola", "goodbye": "adios"};
    string greeting = "hello";
    println(translations{greeting} ++ "!");
    """
    expected6 = "hola!"
    run_bytecode_test(code6, expected6)
    
    # Dictionary updates in a loop
    print("Testing dictionary updates in a loop...")
    code7 = """
    dict counters = {"a": 0, "b": 0, "c": 0};
    string[] letters = ["a", "b", "a", "c", "b", "a"];
    int i = 0;
    while (i < len(letters)) {
        string letter = letters[i];
        counters{letter} = counters{letter} + 1;
        i = i + 1;
    }
    println(counters{"a"});
    println(counters{"b"});
    println(counters{"c"});
    """
    expected7 = "3\n2\n1"
    run_bytecode_test(code7, expected7)
    
    # Dictionary with integer keys
    print("Testing dictionary with integer keys...")
    code8 = """
    dict numMap = {1: "one", 2: "two", 3: "three"};
    int key = 2;
    println(numMap{key});
    """
    expected8 = "two"
    run_bytecode_test(code8, expected8)
    
    # Dictionary with lists as values
    # print("Testing dictionary with list values...")
    # code9 = """
    # dict inventory = {
    #     "weapons": [1, 2, 3],
    #     "potions": [10, 20]
    # };
    # println(inventory{"weapons"}[1]);
    # println(inventory{"potions"}[0]);
    
    # # Modify list inside dictionary
    # inventory{"weapons"}[2] = 99;
    # println(inventory{"weapons"}[2]);
    # """
    # expected9 = "2\n10\n99"
    # run_bytecode_test(code9, expected9)

def test_multidimensional_arrays():
    print("\n===== Testing Multidimensional Arrays =====")
    
    # Basic 2D array creation and access
    print("Testing 2D array creation and access...")
    code1 = """
    int[][] matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    println(matrix[1][2]);
    """
    expected1 = "6"
    run_bytecode_test(code1, expected1)
    
    # Nested array element assignment
    print("Testing nested array element assignment...")
    code2 = """
    int[][] grid = [[1, 2], [3, 4]];
    grid[0][1] = 99;
    println(grid[0][1]);
    """
    expected2 = "99"
    run_bytecode_test(code2, expected2)
    
    # 3D array access
    print("Testing 3D array access...")
    code3 = """
    int[][][] cube = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]];
    println(cube[1][0][1]);
    """
    expected3 = "6"
    run_bytecode_test(code3, expected3)
    
    # Array operations with nested access
    print("Testing nested array calculations...")
    code4 = """
    int[][] data = [[10, 20], [30, 40]];
    int result = data[0][0] + data[1][1];
    println(result);
    """
    expected4 = "50"
    run_bytecode_test(code4, expected4)
    
    # Modifying nested arrays in loops
    print("Testing nested array modification in loops...")
    code5 = """
    int[][] grid = [[0, 0], [0, 0]];
    int i = 0;
    while (i < 2) {
        int j = 0;
        while (j < 2) {
            grid[i][j] = i * 2 + j;
            j = j + 1;
        }
        i = i + 1;
    }
    
    println(grid[0][0]);
    println(grid[0][1]);
    println(grid[1][0]);
    println(grid[1][1]);
    """
    expected5 = "0\n1\n2\n3"
    run_bytecode_test(code5, expected5)

# Update the run_tests function to include the dictionary test
def run_tests():
    try:
        test_arithmetic()
        test_variables()
        test_strings()
        test_conditionals()
        test_loops()
        test_arrays()
        test_dictionaries()  
        test_multidimensional_arrays()
        print("\nAll bytecode compilation tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_tests()
