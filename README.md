# Simple Programming Language Interpreter

## Features

* Basic Operations
  * Arithmetic: `+`, `-`, `*`, `/`, `%`, `**` (power)
  * String: `++` (concatenation)
  * Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
  * Logical: `and`, `or`

* Control Structures
  * If-then-else expressions
  * Function definitions and calls
  * Let expressions for scoping
  * Multi-statement blocks with semicolons

* Environment Handling
  * Lexical scoping
  * Function scope
  * Variable assignments
  * Recursive functions

## Syntax Examples

### Basic Operations
```
# Arithmetic
2 + 3 * 4       # 14
2 ** 3          # 8 (power)
17 % 5          # 2 (modulo)

# Strings
"Hello" ++ " World"  # "Hello World"

# Comparisons and Logic
x > y and z < 10
a >= 5 or b <= 3
```

### Control Flow
```
# If expression
if x > 10 then
    x + y
else
    x - y
end

# Let binding
let x be 5 in
    let y be x * 2 in
        x + y    # Returns 15
    end
end
```

### Functions
```
# Simple function
fun double(x) is x + x in
    double(5)    # Returns 10
end

# Recursive function
fun factorial(n) is
    if n <= 1 then 1
    else n * factorial(n - 1)
    end
in
    factorial(5)  # Returns 120
end

# Nested function calls
fun inc(x) is x + 1 in
    inc(inc(5))  # Returns 7
end
```

### Multiple Statements
```
let sum be 0 in
    let i be 1 in
        sum = sum + i;
        i = i + 1
    end
end
```

## Implementation Details

### Environment
* List-based environment for proper function scoping
* Support for nested scopes
* Variable lookup with reversed scope chain
* Automatic scope cleanup

### AST Node Types
* `BinOp`: Binary operations
* `Number`: Numeric literals
* `String`: String literals
* `If`: Conditional expressions
* `Var`: Variable references
* `Assign`: Variable assignments
* `Let`: Let expressions
* `Fun`: Function definitions
* `Call`: Function calls
* `Sequence`: Multiple statements

### Error Handling
* Syntax errors
* Undefined variables
* Invalid function calls
* Missing parameters
* Unterminated strings
* Type mismatches

## Running Tests
```python
# Function tests
fun double(x) is x + x in double(5) end         # Returns 10
fun square(x) is x * x in square(4) end         # Returns 16
fun inc(x) is x + 1 in inc(inc(5)) end         # Returns 7
fun factorial(n) is                             # Returns 120
    if n <= 1 then 1
    else n * factorial(n - 1)
    end
in
    factorial(5)
end
```

## Project Structure
```
compiler/
│
├── main.py         # Core implementation
│   ├── Lexer
│   ├── Parser
│   └── Evaluator
│
└── README.md       # Documentation
```