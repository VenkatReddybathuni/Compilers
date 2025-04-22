# Typed Programming Language Implementation

## Core Features

### Control Flow
* If-then-else expressions with boolean conditions
* While loops with break/continue statements
* Function definitions with type annotations and return values
* Let expressions for variable declarations
* Return statements
* Multiple statement blocks with proper scoping

### Type System
* Static type checking at compile time
* Basic types: `int`, `bool`, `string`
* Array types with indexing and slicing: `int[]`, `string[]`, etc.
* Multi-dimensional arrays: `int[][]`, etc.
* Dictionary type with string keys: `dict`
* User-defined types (structs) with field access
* Type annotations for function parameters and return types
* Explicit type conversion using `str()`
* Strong type checking with no implicit conversions

### Operations
* Arithmetic: `+`, `-`, `*`, `/`, `%`, `**` (power)
* String: `++` (concatenation with strict type checking)
* Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
* Logical: `and`, `or`
* Array concatenation using `+` operator
* Array and string slicing using `[start:end]` syntax

### Data Structures
* Arrays with indexing, slicing, and length operation
* Dictionaries with string keys and arbitrary value types
* User-defined types (structs) with named fields
* Multi-dimensional arrays

### Advanced Features
* First-class functions and closures
* Function inlining optimization
* Peephole optimization (constant folding)
* Bytecode compilation for efficient execution
* Proper lexical scoping
* Variable capture in closures

## User-Defined Functions

Our language provides comprehensive support for user-defined functions, which are a central feature. Functions in our language have:

### Function Definition and Calling

Functions are defined using the `fun` keyword, with explicit parameter types and return type:

```python
# Basic function definition
fun add(x: int, y: int): int {
    return x + y;
}

# Calling the function
int result = add(5, 10);
println(result);  # Prints 15
```

### Function Return Values

All functions must have a specified return type and appropriate return statements:

```python
fun max(a: int, b: int): int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Recursive Functions

The language fully supports recursive function calls:

```python
fun factorial(n: int): int {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n-1);
    }
}

println(factorial(5));  # Prints 120
```

### Functions with Arrays

Functions can take arrays as parameters and return arrays:

```python
fun sumArray(arr: int[]): int {
    int sum = 0;
    int i = 0;
    while(i < len(arr)) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum;
}

int[] numbers = [1, 2, 3, 4, 5];
println(sumArray(numbers));  # Prints 15
```

### Function Closures

The language supports closures, allowing functions to capture variables from their outer scope:

```python
fun makeAdder(x: int): (int) -> int {
    # x is captured in the closure
    fun add(y: int): int {
        return x + y;  # x is from outer function
    }
    return add;
}

var addFive = makeAdder(5);
println(addFive(10));  # Prints 15
```

### Proper Variable Scoping

Functions create their own scope, and parameters are local to the function:

```python
int x = 1;
fun foo(x: int): int {
    x = 2;         # Changes local x, not global x
    return x;
}
println(foo(x));   # Prints 2
println(x);        # Prints 1 (global x is unchanged)
```

## User-Defined Types

Our language supports custom data types through a struct-like syntax:

### Type Definition and Creation

```python
# Define a Person type
type Person { "name": string, "age": int };

# Create an instance
Person p = Person { "name": "Alice", "age": 30 };

# Access fields
println(p{"name"});  # Prints "Alice"
println(p{"age"});   # Prints 30
```

### Field Modification

Fields of user-defined types can be modified:

```python
type Counter { "value": int };
Counter c = Counter { "value": 0 };

# Update the field
c{"value"} = c{"value"} + 1;
println(c{"value"});  # Prints 1
```

### Nested Types

Types can be nested within other types:

```python
type Point { "x": int, "y": int };
type Circle { "center": Point, "radius": int };

Circle c = Circle { 
    "center": Point { "x": 5, "y": 10 }, 
    "radius": 15 
};

println(c{"center"}{"x"});  # Prints 5
```

### Using Types with Functions

Types can be used as function parameters and return values:

```python
type Rectangle { "width": int, "height": int };

fun area(rect: Rectangle): int {
    return rect{"width"} * rect{"height"};
}

Rectangle r = Rectangle { "width": 5, "height": 10 };
println("Area: " ++ str(area(r)));  # Prints "Area: 50"
```

## Array Operations

The language provides rich support for array manipulation:

### Array Creation and Access

```python
# Array creation
int[] numbers = [1, 2, 3, 4, 5];
string[] words = ["hello", "world", "!"];

# Array indexing (zero-based)
println(numbers[0]);  # Prints 1
println(words[0]);    # Prints "hello"

# Array assignment
numbers[1] = 10;
words[1] = "WORLD";
```

### Array Length

```python
int[] arr = [1, 2, 3, 4, 5];
println(len(arr));  # Prints 5
```

### Array Slicing

```python
int[] arr = [1, 2, 3, 4, 5];
int[] sliced = arr[1:4];  # Creates [2, 3, 4]
```

### Array Concatenation

```python
int[] a = [1, 2, 3];
int[] b = [4, 5, 6];
int[] combined = a + b;  # Results in [1, 2, 3, 4, 5, 6]
```

### Multi-dimensional Arrays

```python
int[][] matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
println(matrix[0][1]);  # Prints 2
```

## String Operations

Comprehensive string manipulation features:

### String Concatenation

```python
string greeting = "Hello";
string target = "World";
string message = greeting ++ " " ++ target;  # "Hello World"
```

### String Indexing

```python
string text = "Hello";
println(text[0]);  # Prints "H"
println(text[4]);  # Prints "o"
```

### String Length

```python
string text = "Hello";
println(len(text));  # Prints 5
```

### String Slicing

```python
string s = "hello world";
string sliced = s[1:5];  # "ello"
```

### String Conversion

```python
int num = 42;
string text = str(num);  # Converts int to string: "42"
```

## Dictionary Operations

Support for dictionary data structures with string keys:

```python
# Dictionary creation
dict person = {"name": "Alice", "age": 30, "city": "Wonderland"};

# Accessing dictionary values
string name = person{"name"};  # "Alice"
int age = person{"age"};       # 30

# Updating dictionary values
person{"age"} = 31;
person{"city"} = "New York";
```

## Control Flow

### If-Else Statements

```python
int x = 10;
if (x > 5) {
    println("x is greater than 5");
} else {
    println("x is not greater than 5");
}
```

### While Loops

```python
int i = 0;
while (i < 5) {
    println(i);
    i = i + 1;
}
```

### Break and Continue

```python
int i = 0;
while (i < 10) {
    i = i + 1;
    if (i % 2 == 0) {
        continue;  # Skip even numbers
    }
    if (i > 7) {
        break;     # Exit loop when i > 7
    }
    println(i);    # Prints 1, 3, 5, 7
}
```

## Optimizations

### Function Inlining

The compiler automatically inlines small, non-recursive functions to improve performance:

```python
fun triple(x: int): int {
    return 3 * x;
}

# This will be optimized by inlining the triple function
int result = triple(5);  # Becomes effectively: int result = 3 * 5;
```

### Peephole Optimization

The compiler performs constant folding and other peephole optimizations:

```python
int x = 5 + 3 * 2;  # Compiled as: int x = 11;
bool check = 5 < 10 and 20 > 15;  # Compiled as: bool check = true;
```

## Bytecode Compilation

Our language includes an efficient bytecode compiler and virtual machine for executing programs:

* The bytecode compiler transforms the AST into a sequence of bytecode instructions
* The bytecode VM interprets these instructions more efficiently than direct AST interpretation
* Function inlining and constant folding optimizations are performed during bytecode generation
* The bytecode format includes instruction opcodes, constants, and variable information

### Example Bytecode Execution

Project Euler solutions showcase the efficiency of our bytecode VM:

```
Compiling code...

Bytecode Stats:
Instructions: 21
Constants: 6
Variables: 3
Max Stack Size: 4

Executing bytecode...
Sum of all multiples of 3 or 5 below 1000: 233168

Expected output: Sum of all multiples of 3 or 5 below 1000: 233168
Actual output: Sum of all multiples of 3 or 5 below 1000: 233168
Output matches expected!
```

## Running the Language

### Using the run.sh Script

To execute programs written in our language, use the `run.sh` script:

```bash
./run.sh your_program.txt
```

This script compiles your program and runs it, displaying the output in the terminal.

### Command Line Options

```bash
# Run with bytecode compilation (default)
./run.sh program.txt

# Run with interpreter only (no bytecode)
./run.sh program.txt --interpret

# Run with debug information
./run.sh program.txt --debug

# Run with optimization disabled
./run.sh program.txt --no-optimize
```

## Project Structure
```
/
├── main.py                 # Core language implementation
├── run.sh                  # Script to run programs
├── tests/                  # Test suites
│   ├── __init__.py        # Makes tests a package
│   ├── test_framework.py  # Testing infrastructure
│   ├── unit_tests.py      # Basic language feature tests
│   ├── error_tests.py     # Error handling tests
│   ├── bytecode_tests.py  # Tests for bytecode compilation
│   ├── project_euler_tests.py  # Complex algorithmic tests
│   └── tests.py           # Test runner
├── examples/               # Example programs
│   ├── basics.txt         # Basic language features
│   ├── closures.txt       # Closure and function examples 
│   └── structs.txt        # User-defined types examples
├── LICENSE                # MIT License
└── README.md             # This documentation
```

## Examples from Project Euler

The language is powerful enough to solve complex algorithmic problems. Here are some examples:

### Project Euler #1 - Multiples of 3 or 5
```python
int x = 1;
int sum = 0;
while(x < 1000) {
    if (x % 3 == 0 or x % 5 == 0) {
        sum = sum + x;
    }
    x = x + 1;
}
println("Sum of all multiples of 3 or 5 below 1000: " ++ str(sum));
# Output: Sum of all multiples of 3 or 5 below 1000: 233168
```

### Project Euler #2 - Even Fibonacci Sum
```python
int sum = 0;
int a = 1;
int b = 2;
while (b < 4000000) {
    if (b % 2 == 0) {
        sum = sum + b;
    }
    int temp = a + b;
    a = b;
    b = temp;
}
println("Sum of even-valued Fibonacci terms below 4 million: " ++ str(sum));
# Output: Sum of even-valued Fibonacci terms below 4 million: 4613732
```

### Project Euler #4 - Largest Palindrome Product
```python
int maxpalindrome = 0;
int i = 99;  

while (i >= 10) {
    int j = 99;  
    while (j >= i) {  
        int product = i * j;
        
        if (product <= maxpalindrome) {
            break;
        }
        
        int reversed = 0;
        int temp = product;
        while (temp > 0) {
            reversed = reversed * 10 + temp % 10;
            temp = temp / 10;
        }
        
        if (product == reversed and product > maxpalindrome) {
            maxpalindrome = product;
        }
        j = j - 1;
    }
    i = i - 1;
}

println("Largest palindrome made from the product of two 2-digit numbers: " ++ str(maxpalindrome));
# Output: Largest palindrome made from the product of two 2-digit numbers: 9009
```
