from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from main import parse, BytecodeCompiler, BytecodeVM
from tests.test_framework import capture_stdout 
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

def run_tests():
    try:
        test_arithmetic()
        test_variables()
        test_strings()
        test_conditionals()
        test_loops()
        print("\nAll bytecode compilation tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    run_tests()
