from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from main import parse, BytecodeCompiler, BytecodeVM
from tests.test_framework import capture_stdout

def test_basic_dict():
    print("\n===== Testing Basic Dictionary Operations =====")
    
    # Dictionary creation and access
    print("Testing dictionary creation and access...")
    code1 = """
    dict numbers = {"one": 1, "two": 2, "three": 3};
    println(numbers{"two"});
    """
    expected1 = "2"
    run_dict_test(code1, expected1)
    
    # Dictionary assignment
    print("Testing dictionary assignment...")
    code2 = """
    dict scores = {"math": 95, "science": 87};
    scores{"history"} = 92;
    println(scores{"history"});
    """
    expected2 = "92"
    run_dict_test(code2, expected2)
    
    # Updating dictionary values
    print("Testing dictionary value updates...")
    code3 = """
    dict prices = {"apple": 1, "orange": 2};
    prices{"apple"} = 3;
    println(prices{"apple"});
    """
    expected3 = "3"
    run_dict_test(code3, expected3)
    
    # Using variables as keys and values
    print("Testing variables as keys/values...")
    code4 = """
    string key = "score";
    int value = 100;
    dict game = {key: value};
    println(game{"score"});
    """
    expected4 = "100"
    run_dict_test(code4, expected4)
    
    # Using dictionary values in calculations
    print("Testing dictionary values in calculations...")
    code5 = """
    dict prices = {"item1": 10, "item2": 20};
    int total =  prices{"item1"} + prices{"item2"};
    println(total);
    """
    expected5 = "30"
    run_dict_test(code5, expected5)
    
    # Using function return values in dictionaries
    print("Testing function results in dictionaries...")
    code6 = """
    fun add(x: int): int {
        return x + 5;
    }
    dict results = {"base": 10, "calculated": add(10)};
    println(results{"calculated"});
    """
    expected6 = "15"
    run_dict_test(code6, expected6)

def run_dict_test(code, expected_output):
    """Run a test through bytecode compilation and execution"""
    print("\nTesting code:\n" + code)
    try:
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
        
        # Run the bytecode
        with capture_stdout() as stdout:
            vm = BytecodeVM(bytecode)
            vm.run()
        
        actual_output = stdout.getvalue().strip()
        print(f"\nExpected output: {expected_output}")
        print(f"Actual output: {actual_output}")
        
        assert actual_output == expected_output, f"Output mismatch: Expected '{expected_output}', got '{actual_output}'"
        print("Output matches expected!")
        return bytecode
    except Exception as e:
        print(f"\nError running test: {type(e).__name__}: {e}")
        raise

if __name__ == "__main__":
    try:
        test_basic_dict()
        print("\nAll dictionary bytecode tests passed!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}")