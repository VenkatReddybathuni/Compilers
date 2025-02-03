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

## Environment Implementation

The interpreter uses a list-based environment system for variable and function scoping:

### Structure
```python
# Environment is a list of tuples: [(name, value), ...]
env = [
    ("x", 5),              # Variable binding
    ("f", ("a", body)),    # Function binding: (param_name, function_body)
]
```

### Key Operations

1. **Variable Lookup**
```python
def lookup(env, v):
    # Search from most recent binding (end of list)
    for name, value in reversed(env):
        if name == v:
            return value
    raise ValueError(f"Variable {v} not found")
```

2. **Scope Management**
```python
# Let binding creates new scope
case Let(var, expr, body):
    env.append((var, e(expr, env)))   # Add new binding
    result = e(body, env)             # Evaluate in new scope
    env.pop()                         # Clean up scope
    return result

# Function definition
case Fun(name, param, body, expr):
    env.append((name, (param, body))) # Store function
    result = e(expr, env)            
    env.pop()                         # Clean up
    return result

# Function call
case Call(fname, arg):
    param, body = lookup(env, fname)  # Get function
    env.append((param, e(arg, env)))  # Bind parameter
    result = e(body, env)            # Execute function
    env.pop()                         # Clean up parameter
    return result
```

### Scoping Example
```python
fun double(x) is x + x in  # Binds double -> ("x", body)
    let y be 5 in          # Binds y -> 5
        double(y)          # Creates temporary x -> 5 during call
    end
end

# Environment evolution:
[]                                  # Initial
[("double", ("x", body))]          # After fun
[("double", ...), ("y", 5)]        # After let
[("double", ...), ("y", 5), ("x", 5)] # During function call
[("double", ...), ("y", 5)]        # After function call
[]                                 # Final
```

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