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
* Type annotations for function parameters and return types
* Explicit type conversion using `str()`

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
The interpreter includes comprehensive test suites in `tests.py`:
* Type checking
* String operations
* Function calls
* Control flow
* Error handling

To run all tests:
```bash
python tests.py
```

## Project Structure
```
compiler/
│
├── main.py         # Core implementation
├── tests.py        # Test suites
└── README.md       # Documentation
```

## Running the Interpreter

```bash
python3 tests.py          # Run all test cases
```