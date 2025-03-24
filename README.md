# Typed Programming Language Implementation

## Core Features

### Control Flow
* If-then-else expressions
* While loops with break/continue
* Function definitions with type annotations
* Let expressions for variable declarations
* Return statements
* Multiple statement blocks

### Type System
* Static type checking
* Basic types: `int`, `string`, `bool`
* Array types: `int[]`, `string[]`
* Type annotations for function parameters and return types
* Explicit type conversion using `str()`
* Array and string indexing
* Built-in `len()` function for arrays and strings

### Operations
* Arithmetic: `+`, `-`, `*`, `/`, `%`, `**` (power)
* String: `++` (concatenation with strict type checking)
* Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
* Logical: `and`, `or`

### Basic Syntax Examples

1. Variable Declarations and Types:
```python
int x = 5;                  # Integer declaration
string msg = "hello";       # String declaration
```

2. Arithmetic Operations:
```python
int a = 5 + 3;             # Addition
int b = 10 - 2;            # Subtraction
int c = 4 * 3;             # Multiplication
int d = 15 / 3;            # Division (integer)
int e = 17 % 5;            # Modulo
int f = 2 ** 3;            # Power operation
```

3. String Operations:
```python
string s1 = "Hello";
string s2 = " World";
string s3 = s1 ++ s2;      # String concatenation
string num = str(42);      # Integer to string conversion
```

4. Comparison Operations:
```python
x < y                      # Less than
x > y                      # Greater than
x <= y                     # Less than or equal
x >= y                     # Greater than or equal
x == y                     # Equal to
x != y                     # Not equal to
```

5. Logical Operations:
```python
x > 0 and y < 10          # Logical AND
x < 0 or y > 20           # Logical OR
```

6. Function Definitions:
```python
fun add(x : int) : int {
    return x + 1;
}

fun greet(name : string) : string {
    return "Hello " ++ name;
}
```

7. Control Flow:
```python
if (x > 0) {
    println("Positive");
} else {
    println("Non-positive");
}

while (x < 10) {
    x = x + 1;
    if (x == 5) {
        continue;
    }
    if (x == 8) {
        break;
    }
    println(x);
}
```

8. Multiple Statements and Scoping:
```python
fun process(x : int) : int {
    int a = x + 1;
    int b = a * 2;
    return b;
}
```

### Arrays and Indexing
```python
# Array Declaration and Initialization
int[] numbers = [1, 2, 3, 4, 5];
string[] words = ["hello", "world"];

# Array Indexing
println(numbers[0]);      # Access first element
numbers[1] = 10;         # Modify element

# String Indexing
string text = "Hello";
println(text[0]);        # Prints "H"

# Array Length
println(len(numbers));   # Prints 5
println(len(text));      # Prints 5

# Array in Functions
fun sumArray(arr: int[]) : int {
    int sum = 0;
    int i = 0;
    while(i < len(arr)) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum;
}
```

### Array Slicing
```python
int[] numbers = [1, 2, 3, 4, 5];
int[] slicedNumbers = numbers[1:4];  # Slices the array from index 1 to 3
println(slicedNumbers[0]);           # Prints 2
println(slicedNumbers[1]);           # Prints 3
println(slicedNumbers[2]);           # Prints 4

# String Slicing
string text = "hello world";
string slicedText = text[1:5];       # Slices the string from index 1 to 4
println(slicedText);                 # Prints "ello"
```

## Type Rules

### String Operations
* String concatenation (`++`) requires both operands to be strings
* Use `str()` for explicit conversion of integers to strings
* No implicit type conversion in string operations

Example:
```python
# Correct
"Hello " ++ "World"          # Works
"Number: " ++ str(42)        # Works

# Incorrect
"Error: " ++ 404             # Type Error
"Code" ++ true              # Type Error
```

### Array Type Rules
* Arrays must be initialized with elements of the correct type
* Array indices must be integers
* Array access is bounds-checked at runtime
* Arrays can be passed to and returned from functions
* Arrays maintain their type information (e.g., `int[]`)

Example:
```python
# Correct array usage
int[] arr = [1, 2, 3];
arr[0] = 42;                # Works
println(arr[1]);           # Works

# Type errors
int[] nums = ["hello"];    # Error: Array elements must be int
arr[1] = "string";         # Error: Cannot assign string to int[]
arr["index"];              # Error: Array index must be int

# Bounds checking
arr[5];                    # Runtime error: Index out of bounds
```

### Function Type Checking
* Parameter types must match argument types
* Return type is enforced
* No implicit conversions in function calls

Example:
```python
# Function definition with types
fun greet(name : string) : string {
    return "Hello " ++ name ++ "!";
}

# Correct usage
greet("Alice")              # Works

# Type errors
greet(123)                  # Error: Expected string, got int
```

### Variable Declarations
* Variables must be declared with types
* Types are checked at assignment

Example:
```python
int x = 5;                  # Works
string msg = "Hello";       # Works
int y = "test";            # Error: Type mismatch
```

## Error Handling

### Type Errors
* Mismatched types in operations
* Invalid string concatenation
* Function parameter type mismatches
* Return type violations
* Assignment type mismatches

Example error messages:
```python
"Error: " ++ 404
# Error: String concatenation requires string operands, got str and int

fun process(x : int) : string {
    return x;
}
# Error: Type mismatch: expected string but got int
```


## Implementation Details

### Environment

### Environment Structure
The environment is implemented as a list of tuples (variable name, value):
```python
env = [
    ("x", 5),
    ("y", "hello"),
    ("add", (param_name, param_type, body, return_type))
]
```

### Scoping Rules
1. Variable Lookup:
```python
int x = 5;
{
    int x = 10;            # Creates new scope
    println(x);            # Prints 10
}
println(x);                # Prints 5
```

2. Function Environment:
```python
fun outer(x : int) : int {
    fun inner(y : int) : int {
        return x + y;      # Captures x from outer scope
    }
    return inner(x);
}
```

### Type Checking Implementation
```python
def check_type(value, expected_type):
    if expected_type == "int":
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value)}")
    elif expected_type == "string":
        if not isinstance(value, str):
            raise TypeError(f"Expected string, got {type(value)}")
    return value
```

### String Concatenation Rules
```python
def check_concat_types(left, right):
    if not isinstance(left, str) or not isinstance(right, str):
        raise TypeError(f"String concatenation requires string operands")
    return left + right
```

### Type Checking Examples

1. Function Type Checking:
```python
fun process(x : int) : string {
    return str(x);         # OK: explicit conversion
    return x;              # Error: expected string, got int
}
```

2. Operation Type Checking:
```python
string s = "Hello";
int n = 42;
string good = s ++ " World";     # OK: string ++ string
string bad = s ++ n;             # Error: can't concat string and int
```

3. Return Type Enforcement:
```python
fun calculate(x : int) : int {
    if (x > 0) {
        return x + 1;      # OK: returns int
    } else {
        return "zero";     # Error: expected int, got string
    }
}
```

### Error Handling Examples

1. Type Mismatch:
```python
fun proc(x : string) : int {
    return x;             # Error: Type mismatch: expected int but got string
}
```

2. Invalid Operation:
```python
int x = "hello" + 5;     # Error: cannot add string and int
```

3. Missing Return:
```python
fun noreturn(x : int) : int {
    int y = x + 1;       # Error: function must return a value
}
```

### Implementation Details

The interpreter uses pattern matching for AST evaluation:
```python
match tree:
    case Number(v):
        return int(v)
    case BinOp("+", l, r):
        return e(l, env) + e(r, env)
    case Call(f, x):
        param, param_type, body, return_type = lookup(env, f)
        # Type checking and evaluation...
```

Environment lookup uses reverse list traversal for proper scoping:
```python
def lookup(env, v):
    for u, uv in reversed(env):
        if u == v:
            return uv
    raise ValueError(f"Variable {v} not found")
```

## Example Programs

### String Manipulation
```python
fun makeTitle(text : string) : string {
    return "*** " ++ text ++ " ***";
}

fun error(code : int) : string {
    return "Error " ++ str(code);  # Explicit conversion
}
```

### Type-Safe Functions
```python
fun double(x : int) : int {
    return x + x;
}

fun concat(a : string, b : string) : string {
    return a ++ b;
}
```

## Running Tests

### All Tests
From the main directory:
```bash
python3 -m tests.tests.py
```

### Individual Test Suites
```bash
# Run unit tests only
python3 -m tests.unit_tests.py

# Run Project Euler tests
python3 -m tests.project_euler_tests.py

# Run error handling tests
python3 -m tests.error_tests.py
```

## Project Structure
```
/
├── main.py                 # Core language implementation
├── tests/                  # Test suites
│   ├── __init__.py        # Makes tests a package
│   ├── test_framework.py  # Testing infrastructure
│   ├── unit_tests.py      # Basic language feature tests
│   ├── error_tests.py     # Error handling tests
│   ├── project_euler_tests.py  # Complex algorithmic tests
│   └── tests.py   # Test runner
├── LICENSE                # MIT License
└── README.md             # This documentation
```

## Running the Interpreter

```bash
python3 tests.py          # Run all test cases
```

# Bytecode Compilation Implementation

## Overview
The language supports compilation to bytecode, providing a bridge between interpretation and native machine code. The bytecode implementation offers several advantages:

- **Performance**: Faster execution than pure interpretation
- **Portability**: Same bytecode runs on any platform with our VM
- **Low-level Control**: Enables optimization techniques
- **Debugging**: Clearer insight into code execution

## Bytecode Architecture

### Core Components
The bytecode system consists of three main components:

1. **BytecodeCompiler**: Transforms AST into bytecode instructions
2. **BytecodeVM**: Executes the bytecode instructions
3. **Instruction Set**: Stack-based operations for computation

### Stack-Based Virtual Machine
Our VM uses a stack-based architecture similar to Java's JVM and Python's CPython VM:

- Operations pop operands from the stack and push results back
- Variables are stored in a separate variables array
- Constants are stored in a constant pool
- Control flow managed through labels and jumps

## Instruction Set

### Stack Operations
- `LOAD_CONST <idx>`: Push constant from pool onto stack
- `LOAD_VAR <idx>`: Push variable value onto stack
- `STORE_VAR <idx>`: Store value from stack into variable
- `POP_TOP`: Discard the top value from stack

### Arithmetic Operations
- `BINARY_ADD`: Add top two stack values
- `BINARY_SUB`: Subtract top value from second value
- `BINARY_MUL`: Multiply top two stack values
- `BINARY_DIV`: Integer division
- `BINARY_MOD`: Modulo operation
- `BINARY_POWER`: Power operation (x^y)

### String Operations
- `BINARY_CONCAT`: String concatenation
- `STR_CONVERT`: Convert top of stack to string

### Control Flow
- `JUMP <label>`: Unconditional jump to label
- `JUMP_IF_FALSE <label>`: Jump if top of stack is false
- `LABEL <label>`: Define a jump target

### Array Operations
- `CREATE_ARRAY <size>`: Create array from elements on stack
- `LOAD_ARRAY_ITEM`: Load item from array at index
- `STORE_ARRAY_ITEM`: Store item to array at index
- `GET_LENGTH`: Get length of array or string

### Comparison Operations
- `BINARY_LT`: Less than
- `BINARY_GT`: Greater than
- `BINARY_LE`: Less than or equal
- `BINARY_GE`: Greater than or equal
- `BINARY_EQ`: Equal
- `BINARY_NE`: Not equal

### Logical Operations
- `BINARY_AND`: Logical AND
- `BINARY_OR`: Logical OR

### I/O Operations
- `PRINT`: Print top of stack

## Compilation Process

### AST to Bytecode Translation
Each AST node type is compiled to a sequence of bytecode instructions:

1. **Literals**: Compiled to `LOAD_CONST`
2. **Variables**: Compiled to `LOAD_VAR`/`STORE_VAR`
3. **Operators**: Compiled to respective binary operations
4. **Control Flow**: Compiled to conditional jumps and labels
5. **Functions**: Compiled to parameter setup and jumps

### Type Information
Type information is preserved during compilation:

- Function parameters and return types
- Array element types
- String operations

### Memory Management
The bytecode VM manages:

- **Stack**: For temporary values during computation
- **Variables**: For named storage
- **Constants**: For literals (numbers, strings)
- **Labels**: For control flow targets

## Example: Bytecode Compilation

### Source Code
```python
fun add(x : int, y : int) : int {
    return x + y;
}

fun main() : int {
    int a = 10;
    int b = 20;
    return add(a, b);
}
```

### Bytecode
```
LOAD_CONST 10
STORE_VAR 0
LOAD_CONST 20
STORE_VAR 1
LOAD_VAR 0
LOAD_VAR 1
CALL add
RETURN
```

### Execution
The bytecode is executed by the VM, which manages the stack, variables, and control flow according to the instructions.
