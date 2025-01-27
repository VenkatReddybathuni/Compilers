# Compilers
# Simple Expression Language Compiler

A compiler implementation for a simple expression language that supports arithmetic operations, logical operations, conditionals, variable assignments, and let expressions.

## Features

### Supported Operations
- Arithmetic: `+`, `-`, `*`, `/`, `**` (power), `%` (modulo)
- String: `++` (concatenation)
- Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Logical: `and`, `or`
- Control Flow: `if-then-else`
- Variable Management: `let` expressions, assignments

### Language Constructs

1. **Basic Expressions**
   - Numbers: `123`, `456`
   - Strings: `"Hello World"`
   - Variables: `x`, `y`

2. **Compound Expressions**
   ```
   2 + 3 * 4
   "Hello" ++ " World"
   x >= 10 and y <= 20
   ```

3. **Conditional Statements**
   ```
   if x > 10 then x + y else x - y end
   ```

4. **Let Expressions**
   ```
   let x be 5 in
     let y be x * 2 in
       x + y
     end
   end
   ```

## Implementation Details

The compiler is implemented in Python and consists of three main components:

1. **Lexer**: Converts source code into tokens
2. **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
3. **Evaluator**: Interprets the AST and executes the program

### AST Node Types
- `BinOp`: Binary operations
- `Number`: Numeric literals
- `String`: String literals
- `If`: Conditional expressions
- `Var`: Variable references
- `Assign`: Variable assignments
- `Let`: Let expressions
- `Sequence`: Multiple statements

## Usage Example

```python
# Initialize environment with variables
env = {"x": 15, "y": 10}

# Parse and evaluate expressions
expr = 'if x >= 10 and y <= 20 then x + y else x - y end'
result = e(parse(expr), env)
print(result)  # Output: 25

# Let expression
expr = 'let a be 3 in let b be a + 2 in a + b end end'
result = e(parse(expr))
print(result)  # Output: 8
```

## Error Handling

The compiler includes basic error handling for:
- Syntax errors
- Unterminated strings
- Invalid expressions
- Missing tokens

## Project Structure

```
compiler/
│
├── main.py         # Main implementation
└── README.md       # Documentation
```
