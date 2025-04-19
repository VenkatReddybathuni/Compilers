#!/usr/bin/env python3
import sys
from pathlib import Path

def run_all_tests():
    """Run all test types with a command-line menu"""
    print("=== Compiler Test Runner ===")
    print("Choose a test type to run:")
    print("1. Unit Tests")
    print("2. Bytecode Tests")
    print("3. Error Tests")
    print("4. Reference Algorithm Tests")
    print("5. Project Euler Reference Tests")
    print("6. Project Euler Bytecode Tests")
    print("7. All Tests")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    
    try:
        choice = int(choice)
        
        if choice == 0:
            print("Exiting test runner.")
            return
            
        elif choice == 1:
            print("\nRunning Unit Tests:")
            from tests.unit_tests import run_tests
            run_tests()
            
        elif choice == 2:
            print("\nRunning Bytecode Tests:")
            from tests.bytecode_tests import run_tests
            run_tests()
            
        elif choice == 3:
            print("\nRunning Error Tests:")
            from tests.error_tests import run_tests
            run_tests()
            
        elif choice == 4:
            print("\nRunning Reference Algorithm Tests:")
            from tests.algorithm_tests import run_algorithm_tests
            run_algorithm_tests()
            
        elif choice == 5:
            print("\nRunning Project Euler Reference Tests:")
            from tests.project_euler_reference_tests import run_euler_tests
            run_euler_tests()
            
        elif choice == 6:
            print("\nRunning Project Euler Bytecode Tests:")
            from tests.project_euler_tests import run_tests
            run_tests()
            
        elif choice == 7:
            print("\nRunning All Tests:")
            
            print("\n1. Unit Tests:")
            from tests.unit_tests import run_tests as run_unit_tests
            run_unit_tests()
            
            print("\n2. Bytecode Tests:")
            from tests.bytecode_tests import run_tests as run_bytecode_tests
            run_bytecode_tests()
            
            print("\n3. Error Tests:")
            from tests.error_tests import run_tests as run_error_tests
            run_error_tests()
            
            print("\n4. Reference Algorithm Tests:")
            from tests.algorithm_tests import run_algorithm_tests
            run_algorithm_tests()
            
            print("\n5. Project Euler Reference Tests:")
            from tests.project_euler_reference_tests import run_euler_tests
            run_euler_tests()
            
            print("\n6. Project Euler Bytecode Tests:")
            from tests.project_euler_tests import run_tests as run_euler_bytecode_tests
            run_euler_bytecode_tests()
            
        else:
            print("Invalid choice. Please enter a number from the menu.")
            
    except ValueError:
        print("Invalid input. Please enter a number.")
    except ImportError as e:
        print(f"Error importing test module: {e}")
    except Exception as e:
        print(f"Error running tests: {e}")

if __name__ == "__main__":
    # Add project root to Python path
    sys.path.append(str(Path(__file__).parent))
    
    # If arguments are provided, run specific tests
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        
        if test_type == "unit":
            from tests.unit_tests import run_tests
            run_tests()
        elif test_type == "bytecode":
            from tests.bytecode_tests import run_tests
            run_tests()
        elif test_type == "error":
            from tests.error_tests import run_tests
            run_tests()
        elif test_type == "algorithm":
            from tests.algorithm_tests import run_algorithm_tests
            run_algorithm_tests()
        elif test_type == "euler":
            from tests.project_euler_reference_tests import run_euler_tests
            run_euler_tests()
        elif test_type == "euler_bytecode":
            from tests.project_euler_tests import run_tests
            run_tests()
        elif test_type == "all":
            run_all_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print("Available test types: unit, bytecode, error, algorithm, euler, euler_bytecode, all")
    else:
        run_all_tests()
