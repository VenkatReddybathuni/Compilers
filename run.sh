#!/bin/bash

# Enhanced script to run files in our custom language
# Usage: ./run.sh filename.txt [debug]
# Note: Type checking is now mandatory for all executions

COMPILER_DIR="/home/venkat/Desktop/Compilers"
CODE_FILE="$1"
RUN_OPTION="$2"

# Check if a file argument was provided
if [ -z "$CODE_FILE" ]; then
  echo "Usage: $0 <source_file> [debug]"
  echo "Example: $0 euler.txt"
  echo "Options:"
  echo "  debug     - Enable VM debugging output"
  echo "Note: Static type checking is now mandatory for all code execution"
  exit 1
fi

# Check if the file exists
if [ ! -f "$CODE_FILE" ]; then
  echo "Error: Source file not found: $CODE_FILE"
  exit 1
fi

# Create a wrapper Python script to handle execution more robustly
cat > "$COMPILER_DIR/run_now.py" << EOF
#!/usr/bin/env python3
import sys
import os
from time import time
from pathlib import Path

# Make sure stdout is unbuffered for immediate output
os.environ['PYTHONUNBUFFERED'] = '1'
sys.stdout.reconfigure(line_buffering=True, write_through=True)

# Add parent directory to path
sys.path.append('${COMPILER_DIR}')

# Import required components
from main import parse, BytecodeCompiler, BytecodeVM, TypeChecker, TypeCheckError, compile_with_static_type_check

def run_file(filename, option=None):
    """Run a file with bytecode VM with reliable output flushing"""
    try:
        # Read the source code
        with open(filename, 'r') as f:
            code = f.read()
        
        print(f"Running {filename} with mandatory type checking...")
        debug_mode = option == "debug"
        
        if debug_mode:
            print("Debug mode enabled")
        
        # Parse and compile with mandatory type checking
        start_time = time()
        
        # Always run static type checking
        try:
            bytecode = compile_with_static_type_check(code)
            print("Code type-checked successfully!")
        except TypeCheckError as e:
            print(f"Type Error: {e}")
            return 1
        
        # Run the program
        vm = BytecodeVM(bytecode)
        
        # Set debugging mode for VM if requested
        if debug_mode:
            vm.debug = True
        
        result = vm.run()
        end_time = time()
        
        # Print execution stats
        if debug_mode:
            print(f"\nExecution completed in {end_time - start_time:.4f} seconds")
        
        return 0
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    option = sys.argv[2] if len(sys.argv) > 2 else None
    sys.exit(run_file(sys.argv[1], option))
EOF

# Make the wrapper script executable
chmod +x "$COMPILER_DIR/run_now.py"

# Run the program with Python unbuffered output
PYTHONUNBUFFERED=1 python3 -u "$COMPILER_DIR/run_now.py" "$CODE_FILE" "$RUN_OPTION"

# Clean up
rm "$COMPILER_DIR/run_now.py"

exit $?