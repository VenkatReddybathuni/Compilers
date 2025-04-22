from dataclasses import dataclass
from collections.abc import Iterator

class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class Number(AST):
    val: str

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST

@dataclass
class Var(AST):
    name: str

@dataclass
class Assign(AST):
    name: str
    e: AST

@dataclass
class String(AST):
    val: str

@dataclass
class Let(AST):
    var: str
    expr: AST
    body: AST
    var_type: str = None  # Add var_type field with default None

@dataclass
class Sequence(AST):
    statements: list[AST]

@dataclass
class Fun(AST):
    n: str       # name
    params: list[tuple[str, str]]  # list of (param_name, param_type) tuples
    rt: str      # return type
    b: AST       # body
    e: AST       # expression

@dataclass
class Call(AST):
    n: str       # function name
    args: list   # list of arguments

@dataclass
class Closure(AST):
    params: list         # list of (param_name, param_type) tuples
    body: AST           # function body
    return_type: str    # return type
    captured_env: list  # captured environment

@dataclass
class PrintLn(AST):
    expr: AST

@dataclass
class Return(AST):
    expr: AST

@dataclass
class StrConversion(AST):
    expr: AST

@dataclass
class While(AST):
    cond: AST
    body: AST

@dataclass
class Continue(AST):
    pass

@dataclass
class Break(AST):
    pass

@dataclass
class Array(AST):
    elements: list[AST]

@dataclass
class ArrayAccess(AST):
    array: AST
    indices: list[AST]  # Changed from single index to list of indices for multi-dimensional access

@dataclass
class ArrayAssign(AST):
    array: AST
    indices: list[AST]  # Changed from single index to list of indices
    value: AST

@dataclass
class Length(AST):
    expr: AST

@dataclass
class Dict(AST):
    pairs: list[tuple[AST, AST]]

@dataclass
class DictAccess(AST):
    dict: AST
    key: AST

@dataclass
class DictAssign(AST):
    dict: AST
    key: AST
    value: AST

@dataclass
class Slice(AST):
    sequence: AST
    start: AST
    end: AST


@dataclass
class TypeDef(AST):
    name: str
    fields: dict  # Maps field name to type name

@dataclass
class TypeInstantiation(AST):
    type_name: str
    fields: Dict

class Token:
    pass

@dataclass
class NumberToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class KeywordToken(Token):
    w: str

@dataclass
class VarToken(Token):
    v: str

@dataclass
class StringToken(Token):
    v: str

@dataclass
class TypeToken(Token):
    t: str
    is_array: bool = False  # Add array type flag
    array_dimensions: int = 0  # Track number of dimensions for nd arrays 

@dataclass
class TypeDefToken(Token):
    name: str

@dataclass
class TypeDefToken(Token):
    name: str

@dataclass
class ArrayToken(Token):
    elements: list[Token]

@dataclass
class TypeCheckError(Exception):
    """An error raised during type checking"""
    message: str
    node: AST = None  # The AST node that caused the error
    
    def __str__(self):
        return self.message

class TypeChecker:
    """A static type checker for our language"""
    
    def __init__(self):
        self.environment = {}  # Maps variable names to their types
        self.function_env = {}  # Maps function names to their signatures
        self.current_function = None  # Current function being checked
        self.return_type = None  # Expected return type of current function
        self.errors = []
    
    def check(self, ast):
        """Perform type checking on the entire AST"""
        self._check_node(ast, scope={})
        
        if self.errors:
            # Report the first error
            raise self.errors[0]
            
        return True
    
    def _check_node(self, node, scope):
        """Recursively check types in the AST"""
        if node is None:
            return "void"
            
        match node:
            case Number(_):
                return "int"
                
            case String(_):
                return "string"
                
            case Var(name):
                # Check if variable exists in scope or environment
                if name in scope:
                    return scope[name]
                elif name in self.environment:
                    return self.environment[name]
                else:
                    self.errors.append(TypeCheckError(f"Undefined variable '{name}'", node))
                    return "unknown"
                
            case BinOp(op, left, right):
                left_type = self._check_node(left, scope)
                right_type = self._check_node(right, scope)
                
                # Handle string concatenation
                if op == "++":
                    if left_type != "string" or right_type != "string":
                        self.errors.append(TypeCheckError(
                            f"String concatenation (++) requires string operands, got '{left_type}' and '{right_type}'", node))
                        return "string"  # Assume string anyway to avoid cascade errors
                    return "string"
                
                # Handle comparison operators
                if op in ["<", ">", "<=", ">=", "==", "!="]:
                    # Type compatibility for comparisons
                    if left_type != right_type:
                        self.errors.append(TypeCheckError(
                            f"Cannot compare '{left_type}' with '{right_type}'", node))
                    return "bool"
                
                # Handle logical operators
                if op in ["and", "or"]:
                    # Both operands should be boolean
                    if left_type != "bool" or right_type != "bool":
                        self.errors.append(TypeCheckError(
                            f"Logical operator '{op}' requires boolean operands, got '{left_type}' and '{right_type}'", node))
                    return "bool"
                
                # Handle arithmetic operators
                if op in ["+", "-", "*", "/", "%", "**"]:
                    # Both operands should be numeric
                    if left_type != "int" or right_type != "int":
                        self.errors.append(TypeCheckError(
                            f"Arithmetic operator '{op}' requires int operands, got '{left_type}' and '{right_type}'", node))
                    return "int"
                
                # Unknown operator
                self.errors.append(TypeCheckError(f"Unknown operator '{op}'", node))
                return "unknown"
                
            case If(cond, then, else_):
                cond_type = self._check_node(cond, scope)
                
                # Condition must be a boolean
                if cond_type != "bool":
                    self.errors.append(TypeCheckError(
                        f"If condition must be boolean, got '{cond_type}'", cond))
                
                # Check both branches
                then_type = self._check_node(then, scope)
                else_type = self._check_node(else_, scope)
                
                # If expression returns the same type from both branches
                if then_type != else_type:
                    self.errors.append(TypeCheckError(
                        f"If branches must have the same type, got '{then_type}' and '{else_type}'", node))
                    return "unknown"
                    
                return then_type
                
            case Let(var, expr, body, var_type):
                # Check the initialization expression
                expr_type = self._check_node(expr, scope)
                
                # If variable type is specified, verify it matches expr_type
                if var_type and expr_type != var_type:
                    self.errors.append(TypeCheckError(
                        f"Cannot assign {expr_type} to variable '{var}' of type {var_type}", node))
                
                # Add the variable to scope for the body
                new_scope = scope.copy()
                new_scope[var] = var_type if var_type else expr_type
                self.environment[var] = var_type if var_type else expr_type
                
                # Check the body with the updated scope
                return self._check_node(body, new_scope)
                
            case Assign(name, expr):
                expr_type = self._check_node(expr, scope)
                
                # Check if variable exists and has the right type
                if name in scope:
                    var_type = scope[name]
                    if var_type != expr_type:
                        self.errors.append(TypeCheckError(
                            f"Cannot assign {expr_type} to variable '{name}' of type {var_type}", node))
                elif name in self.environment:
                    var_type = self.environment[name]
                    if var_type != expr_type:
                        self.errors.append(TypeCheckError(
                            f"Cannot assign {expr_type} to variable '{name}' of type {var_type}", node))
                else:
                    self.errors.append(TypeCheckError(f"Undefined variable '{name}'", node))
                
                return expr_type
                
            case Fun(n, params, rt, b, e):
                # Store function signature in environment
                param_types = [(param_name, param_type) for param_name, param_type in params]
                self.function_env[n] = (param_types, rt)
                
                # Create a new scope for function parameters
                func_scope = scope.copy()
                for param_name, param_type in params:
                    func_scope[param_name] = param_type
                
                # Save current function context
                prev_function = self.current_function
                prev_return_type = self.return_type
                self.current_function = n
                self.return_type = rt
                
                # Check function body
                self._check_node(b, func_scope)
                
                # Restore function context
                self.current_function = prev_function
                self.return_type = prev_return_type
                
                # Continue with code after function definition
                return self._check_node(e, scope)
                
            case Call(n, args):
                # Check if the function exists
                if n not in self.function_env:
                    self.errors.append(TypeCheckError(f"Undefined function '{n}'", node))
                    return "unknown"
                
                # Get function signature
                func_sig = self.function_env[n]
                param_types = func_sig[0]
                return_type = func_sig[1]
                
                # Check argument count
                if len(args) != len(param_types):
                    self.errors.append(TypeCheckError(
                        f"Function '{n}' expects {len(param_types)} arguments, got {len(args)}", node))
                else:
                    # Check argument types
                    for i, (arg, (_, expected_type)) in enumerate(zip(args, param_types)):
                        arg_type = self._check_node(arg, scope)
                        if arg_type != expected_type:
                            self.errors.append(TypeCheckError(
                                f"Function '{n}' argument {i+1} expects {expected_type}, got {arg_type}", arg))
                
                return return_type
                
            case Return(expr):
                expr_type = self._check_node(expr, scope)
                
                # Check if return type matches function return type
                if self.current_function and self.return_type and expr_type != self.return_type:
                    self.errors.append(TypeCheckError(
                        f"Function '{self.current_function}' expects return type {self.return_type}, got {expr_type}", node))
                
                return expr_type
                
            case Sequence(statements):
                result_type = "void"
                for stmt in statements:
                    result_type = self._check_node(stmt, scope)
                return result_type
                
            case PrintLn(expr):
                # PrintLn can accept any type
                self._check_node(expr, scope)
                return "void"
                
            case StrConversion(expr):
                # str() can convert int or string
                expr_type = self._check_node(expr, scope)
                if expr_type not in ["int", "string"]:
                    self.errors.append(TypeCheckError(
                        f"str() only supports int and string types, got {expr_type}", node))
                return "string"
                
            case While(cond, body):
                cond_type = self._check_node(cond, scope)
                
                # Condition must be a boolean
                if cond_type != "bool":
                    self.errors.append(TypeCheckError(
                        f"While condition must be boolean, got '{cond_type}'", cond))
                
                # Check the loop body
                self._check_node(body, scope)
                return "void"
                
            case Array(elements):
                if not elements:
                    return "int[]"  # Default for empty arrays
                    
                # Check that all array elements have the same type
                elem_types = [self._check_node(elem, scope) for elem in elements]
                if len(set(elem_types)) != 1:
                    self.errors.append(TypeCheckError(
                        f"Array elements must have the same type, got {set(elem_types)}", node))
                    return "unknown[]"
                
                return f"{elem_types[0]}[]"
                
            case ArrayAccess(array, indices):
                array_type = self._check_node(array, scope)
                index_types = [self._check_node(index, scope) for index in indices]
                
                # Check that all indices are integers
                if not all(index_type == "int" for index_type in index_types):
                    self.errors.append(TypeCheckError(
                        f"Array indices must be int, got {index_types}", indices))
                
                # Check that array is actually an array
                if not array_type.endswith("[]"):
                    self.errors.append(TypeCheckError(
                        f"Cannot index into non-array type {array_type}", array))
                    return "unknown"
                
                # Return element type
                return array_type[:-2]  # Remove '[]'
                
            case _:
                # Default case for other node types
                return "unknown"

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class TypeError(Exception):
    pass

class LoopControl(Exception):
    pass

class ContinueLoop(LoopControl):
    pass

class BreakLoop(LoopControl):
    pass

def check_concat_types(left, right):
    """Stricter type checking for string concatenation"""
    if not isinstance(left, str) or not isinstance(right, str):
        raise TypeError(f"String concatenation requires string operands, got {type(left).__name__} and {type(right).__name__}")
    return left + right

def convert_to_string(value, context=""):
    """Explicit string conversion with type checking"""
    if isinstance(value, (int, str)):
        return str(value)
    raise TypeError(f"{context}Cannot convert {type(value).__name__} to string")

# Dictionary to store user-defined types
user_defined_types = {}

def check_type(value, expected_type):
    if '[' in expected_type:  # Handle array types
        base_type = expected_type.split('[')[0].strip()
        if not isinstance(value, list):
            raise TypeError(f"Type mismatch: expected {expected_type} but got {type(value).__name__}")
        if base_type == "int":
            if not all(isinstance(x, int) for x in value):
                raise TypeError(f"Array elements must be {base_type}")
        elif base_type == "string":
            if not all(isinstance(x, str) for x in value):
                raise TypeError(f"Array elements must be {base_type}")
        return value
    
    # Handle user-defined types
    if expected_type in user_defined_types:
        if not isinstance(value, dict):
            raise TypeError(f"Type mismatch: expected {expected_type} but got {type(value).__name__}")
        # Additional type checking could be done here
        return value
    
    if expected_type == "any":  # Special case for len() function
        return value
    elif expected_type == "int":
        if not isinstance(value, int):
            raise TypeError(f"Type mismatch: expected int but got {type(value).__name__}")
    elif expected_type == "string":
        if not isinstance(value, str):
            raise TypeError(f"Type mismatch: expected string but got {type(value).__name__}")
    elif expected_type == "bool":
        if not isinstance(value, bool):
            raise TypeError(f"Type mismatch: expected bool but got {type(value).__name__}")
    return value

def lookup(env, v):
    # Add built-in functions
    if v == "len":
        # Create a special closure for the len function
        params = [("obj", "any")]
        body = Length(Var("obj"))
        return Closure(params, body, "int", [])
    
    # First check in local environment
    env_reversed = list(reversed(env))
    for u, uv in env_reversed:
        if u == v:
            return uv
    
    # If not found, check in global environment (first binding in the environment)
    for u, uv in env:
        if u == v:
            return uv
    
    raise ValueError(f"Variable {v} not found")


def update_env(env, name, value):
    """Update an existing variable in the environment or add it if doesn't exist"""
    for i, (var, _) in enumerate(env):
        if var == name:
            env[i] = (name, value)
            return
    env.append((name, value))
def e(tree: AST, env=None) -> int | bool | str | list | dict:
    if env is None:
        env = []  # Empty list for environment

    match tree:
        case PrintLn(expr):
            result = e(expr, env)
            print(result, flush=True)  # Added flush=True to ensure immediate output
            return result
        case Number(v):
            return int(v)
        case Var(v):
            return lookup(env, v)
        case Fun(f, params, rt, b, c):
            # Create a closure with the current environment captured
            # For recursive functions, we need to include the function name in its own environment
            function_env = env.copy()
            closure = Closure(params, b, rt, function_env)
            
            # Add the function to the environment BEFORE creating the closure
            # This allows recursive calls to find the function
            update_env(env, f, closure)
            
            # Store function name in closure's environment for recursion
            update_env(closure.captured_env, f, closure)
            
            return e(c, env)
        case Call(f, args):
            # Get the function object
            func_obj = lookup(env, f)
            
            # Evaluate arguments in the caller's environment
            arg_values = [e(arg, env) for arg in args]
            
            if isinstance(func_obj, Closure):
                # Handle closure with captured environment
                params = func_obj.params
                param_names = [param_name for param_name, _ in params]
                param_types = [param_type for _, param_type in params]
                body = func_obj.body
                return_type = func_obj.return_type
                
                # Start with the captured environment from when function was defined
                call_env = func_obj.captured_env.copy()
                
                # Check that the number of arguments matches the number of parameters
                if len(arg_values) != len(params):
                    raise TypeError(f"Function '{f}' expected {len(params)} arguments but got {len(arg_values)}")
                
                # Type checking and binding for all arguments
                for i, ((param_name, param_type), arg_value) in enumerate(zip(params, arg_values)):
                    if param_type == "string" and isinstance(arg_value, int):
                        arg_value = str(arg_value)
                    elif param_type == "int" and isinstance(arg_value, str):
                        raise TypeError(f"Function '{f}' parameter {i+1} expects int but got string")
                    
                    try:
                        check_type(arg_value, param_type)
                    except TypeError as te:
                        raise TypeError(f"Function '{f}' parameter {i+1} type mismatch: {str(te)}")
                    
                    # Add parameter binding to the closure environment
                    update_env(call_env, param_name, arg_value)
            
            else:
                raise TypeError(f"Cannot call {f}, not a function")
            
            try:
                result = e(body, call_env)
                return check_type(result, return_type)
            except ReturnValue as rv:
                return check_type(rv.value, return_type)
        case BinOp("+", l, r):
            return e(l, env) + e(r, env)
        case BinOp("-", l, r):
            return e(l, env) - e(r, env)
        case BinOp("*", l, r):
            return e(l, env) * e(r, env)
        case BinOp("/", l, r):
            return e(l, env) // e(r, env)
        case BinOp("<", l, r):
            return e(l, env) < e(r, env)
        case BinOp("<=", l, r):
            return e(l, env) <= e(r, env)
        case BinOp(">=", l, r):
            return e(l, env) >= e(r, env)
        case BinOp("==", l, r):
            return e(l, env) == e(r, env)
        case BinOp("!=", l, r):
            return e(l, env) != e(r, env)
        case BinOp("and", l, r):
            return e(l, env) and e(r, env)
        case BinOp("or", l, r):
            return e(l, env) or e(r, env)
        case BinOp("%", l, r):
            return e(l, env) % e(r, env)
        case BinOp("**", l, r):
            return e(l, env) ** e(r, env)
        case String(v):
            return v
        case BinOp("++", l, r):  
            left_val = e(l, env)
            right_val = e(r, env)

            # No automatic conversion - both must be strings
            if not isinstance(left_val, str) or not isinstance(right_val, str):
                raise TypeError(f"Cannot concatenate {type(left_val).__name__} with {type(right_val).__name__}. Use str() for explicit conversion")

            return left_val + right_val
        case BinOp(">", l, r):
            return e(l, env) > e(r, env)
        case If(cond, then, else_):
            if e(cond, env):
                return e(then, env)
            else:
                return e(else_, env)
        case Sequence(statements):
            result = None
            for stmt in statements:
                result = e(stmt, env)
            return result
        case Assign(name, expr):
            value = e(expr, env)
            update_env(env, name, value)
            return value
        case Let(var, expr, body):
            value = e(expr, env)  
            update_env(env, var, value)  # Update or add variable
            return e(body, env) 
        case Return(expr):
            result = e(expr, env)
            raise ReturnValue(result)
        case StrConversion(expr):
            val = e(expr, env)
            return str(val)
        case While(cond, body):
            result = None
            while e(cond, env):
                try:
                    result = e(body, env)
                except ContinueLoop:
                    continue
                except BreakLoop:
                    break      
            return result if result is not None else 0
        case Continue():
            raise ContinueLoop()
        case Break():
            raise BreakLoop()
        case Array(elements):
            # Get array type from context if available
            array_type = None
            if isinstance(tree.parent, Let):
                array_type = tree.parent.var_type  # You'll need to add var_type to Let
            values = [e(elem, env) for elem in elements]
            # Type check array elements
            if array_type:
                base_type = array_type.split('[')[0].strip()
                if base_type == "int" and not all(isinstance(x, int) for x in values):
                    raise TypeError("Array elements must be int")
                elif base_type == "string" and not all(isinstance(x, str) for x in values):
                    raise TypeError("Array elements must be string")
            return values
        case ArrayAccess(array, indices):
            arr = e(array, env)
            idxs = [e(index, env) for index in indices]
            for idx in idxs:
                if isinstance(arr, (list, str)):
                    if 0 <= idx < len(arr):
                        arr = arr[idx]
                    else:
                        raise IndexError("Array index out of bounds")
                else:
                    raise TypeError(f"Cannot index into {type(arr).__name__}")
            return arr
        case ArrayAssign(array, indices, value):
            arr = e(array, env)
            idxs = [e(index, env) for index in indices]
            val = e(value, env)
            
            # Find array type from environment
            array_name = array.name if isinstance(array, Var) else None
            if array_name:
                for var, stored_val in reversed(env):
                    if var == array_name:
                        # Check element type
                        if isinstance(stored_val, list):
                            if stored_val and isinstance(stored_val[0], int):
                                if not isinstance(val, int):
                                    raise TypeError("Cannot assign non-int to int[]")
                            elif stored_val and isinstance(stored_val[0], str):
                                if not isinstance(val, str):
                                    raise TypeError("Cannot assign non-string to string[]")
                        break

            for idx in idxs[:-1]:
                if not isinstance(idx, int):
                    raise TypeError("Array index must be integer")
                if isinstance(arr, list):
                    if 0 <= idx < len(arr):
                        arr = arr[idx]
                    else:
                        raise IndexError("Array index out of bounds")
                else:
                    raise TypeError("Cannot assign to non-array type")
            
            final_idx = idxs[-1]
            if not isinstance(final_idx, int):
                raise TypeError("Array index must be integer")
            if isinstance(arr, list):
                if 0 <= final_idx < len(arr):
                    arr[final_idx] = val
                    return val
                raise IndexError("Array index out of bounds")
            raise TypeError("Cannot assign to non-array type")
        case Length(expr):
            val = e(expr, env)
            if isinstance(val, (list, str)):
                return len(val)
            raise TypeError(f"Cannot get length of {type(val).__name__}")
        case Slice(sequence, start, end):
            seq = e(sequence, env)
            start_idx = e(start, env)
            end_idx = e(end, env)
            if isinstance(seq, (list, str)):
                return seq[start_idx:end_idx]
            raise TypeError(f"Cannot slice {type(seq).__name__}")
        case Dict(pairs):
            return {e(key, env): e(value, env) for key, value in pairs}
        case DictAccess(dict, key):
            d = e(dict, env)
            k = e(key, env)
            return d[k]
        case DictAssign(dict, key, value):
            d = e(dict, env)
            k = e(key, env)
            v = e(value, env)
            d[k] = v
            return v
        case TypeDef(name, fields):
            # Register the type definition
            user_defined_types[name] = fields
            return None
            
        case TypeInstantiation(type_name, fields):
            # Check if the type exists
            if type_name not in user_defined_types:
                raise TypeError(f"Unknown type: {type_name}")
            
            type_def = user_defined_types[type_name]
            # Create an empty dict for the instance
            instance = {}
            
            # Evaluate fields Dict and extract the pairs
            fields_dict = e(fields, env)
            
            # Check for missing required fields
            for field_name in type_def:
                if field_name not in fields_dict:
                    raise TypeError(f"Missing required field '{field_name}' for type {type_name}")
                    
            # Check for extra fields
            for field_name in fields_dict:
                if field_name not in type_def:
                    raise TypeError(f"Unknown field '{field_name}' for type {type_name}")
            
            # Type check and populate the instance
            for field_name, field_value in fields_dict.items():
                expected_type = type_def[field_name]
                # Type check the field value
                try:
                    typed_value = check_type(field_value, expected_type)
                    instance[field_name] = typed_value
                except TypeError as te:
                    raise TypeError(f"Field '{field_name}' type mismatch: {str(te)}")
                
            # Return the instance as a dict
            return instance
        case Closure(params, body, return_type, _):
            # When a closure appears directly in code (not via Fun), capture the current env
            return Closure(params, body, return_type, env.copy())

def lex(s: str) -> Iterator[Token]:
    i = 0
    while i < len(s):  
        while i < len(s) and s[i].isspace():
            i += 1

        if i >= len(s):
            return

        if s[i].isalpha():
            t = s[i]
            i = i + 1
            while i < len(s) and (s[i].isalpha() or s[i].isdigit() or s[i] == '_'):  # Allow digits and underscores in identifiers 
                t = t + s[i]
                i = i + 1
            # print(t)
            # Check if this is an array type (e.g. "int[]")
            is_array = False
            array_dimensions = 0
            while i + 1 < len(s) and s[i] == '[' and s[i + 1] == ']':
                is_array = True
                array_dimensions += 1
                i += 2
                
            if t in {"and", "or", "if", "else", "fun", "return", "println", "str", "while", "continue", "break", "dict", "type"}:  # Added "type"
                yield KeywordToken(t)
            elif t in {"int", "float", "string", "void", "bool"}:  # Types are now handled separately
                yield TypeToken(t, is_array, array_dimensions)
            else:
                yield VarToken(t)
        elif s[i].isdigit():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isdigit():
                t = t + s[i]
                i = i + 1
            yield NumberToken(t)
        elif s[i] == '"':  
            t = ""
            i += 1
            while i < len(s) and s[i] != '"':
                t += s[i]
                i += 1
            if i < len(s):  
                i += 1
                yield StringToken(t)
            else:
                raise ParseError("Unterminated string literal")
        else:
            match t := s[i]:
                case '+' | '*' | '<' | '=' | '-' | '/' | '%' | '>' | '!' | '(' | ')' | ';' | '{' | '}' | ':' | '[' | ']' | ',':  # Added comma
                    i += 1
                    if i < len(s):
                        next_char = s[i]
                        if (t + next_char) in {'**', '++', '<=', '>=', '==', '!='}: 
                            t += next_char
                            i += 1
                    yield OperatorToken(t)
                case _:
                    raise ParseError(f"Unexpected character: {t}")


class ParseError(Exception):
    pass

def parse(s: str) -> AST:
    from more_itertools import peekable
    tokens = list(lex(s))
    t = peekable(tokens)
    
    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError(f"Expected {what} but got {t.peek(None)}")
    
    def parse_statements():
        statements = []
        while t.peek(None) is not None:
            if isinstance(t.peek(), OperatorToken) and t.peek().o == '}':
                break

            stmt = parse_stmt()
            #print(stmt)
            statements.append(stmt)

            # Handle semicolons more carefully
            if isinstance(t.peek(None), OperatorToken) and t.peek().o == ';':
                next(t)

        # Always return a Sequence for multiple statements
        if len(statements) > 1:
            return Sequence(statements)
        elif len(statements) == 1:
            return statements[0]
        else:
            return Number("0")  # Empty block returns 0

    def parse_stmt():
        # print(f"parse_stmt: {t.peek(None)}")  # Debugging statement
        match t.peek(None):
            
            case VarToken(var) if var in user_defined_types:
                # This is a type declaration using a user-defined type
                type_name = next(t).v  # consume the type name (e.g. "Person")
                
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError(f"Expected variable name after type {type_name}")
                
                var_name = next(t).v  # consume the variable name (e.g. "p")
                
                expect(OperatorToken("="))
                
                # Now we expect the type name again for instantiation
                if not isinstance(t.peek(None), VarToken) or t.peek().v != type_name:
                    raise ParseError(f"Expected type {type_name} for instantiation")
                
                next(t)  # consume the type name again
                
                # Parse instantiation body { "field1": value1, ... }
                expect(OperatorToken("{"))
                pairs = []
                
                while t.peek(None) != OperatorToken("}"):
                    # Field key must be a string literal
                    if not isinstance(t.peek(None), StringToken):
                        raise ParseError("Expected field name as string literal")
                    key = String(next(t).v)
                    
                    expect(OperatorToken(":"))
                    value = parse_expr()
                    pairs.append((key, value))
                    
                    if t.peek(None) == OperatorToken(","):
                        next(t)
                        # Check if there's another field after comma
                        if t.peek(None) == OperatorToken("}"):
                            break
                    # No need to check for closing brace here - let the loop condition handle it
                
                expect(OperatorToken("}"))
                
                # Create the type instantiation
                type_inst = TypeInstantiation(type_name, Dict(pairs))
                
                # Assign to variable
                expect(OperatorToken(";"))
                next_stmt = parse_statements() if t.peek(None) is not None else None
                return Let(var_name, type_inst, next_stmt if next_stmt else Sequence([]), type_name)

            case TypeToken(typ, is_array, array_dimensions):
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError(f"Expected variable name after {typ}")
                var = next(t).v
                var_type = f"{typ}{'[]' * array_dimensions}" if is_array else typ
                expect(OperatorToken("="))
                
                if is_array:
                    if isinstance(t.peek(None), VarToken):
                        array_name = next(t).v
                        expect(OperatorToken("["))
                        start = parse_expr()
                        expect(OperatorToken(":"))
                        end = parse_expr()
                        expect(OperatorToken("]"))
                        array_expr = Slice(Var(array_name), start, end)
                    elif isinstance(t.peek(None), OperatorToken) and t.peek().o == '[':
                        array_expr = parse_atom()
                    else:
                        raise ParseError(f"Expected array literal or slice after {var}")
                    
                    let_node = Let(var, array_expr, None, var_type)
                    array_expr.parent = let_node
                    expect(OperatorToken(";"))
                    next_stmt = parse_statements() if t.peek(None) is not None else None
                    let_node.body = next_stmt if next_stmt else Sequence([])
                    return let_node
                
                # Allow any expression, including complex expressions with dictionary lookups
                expr = parse_expr()
                expect(OperatorToken(";"))
                next_stmt = parse_statements() if t.peek(None) is not None else None
                return Let(var, expr, next_stmt if next_stmt else Sequence([]))
                
            case KeywordToken("fun"):
                next(t)  # Consume "fun" keyword
                
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError("Expected function name")
                name = next(t).v
                
                expect(OperatorToken("("))
                
                # Parse parameters - handle multiple parameters
                params = []
                
                # If there's a first parameter
                if isinstance(t.peek(None), VarToken):
                    param_name = next(t).v
                    
                    # Parse parameter type
                    expect(OperatorToken(":"))
                    if not isinstance(t.peek(None), TypeToken):
                        if isinstance(t.peek(None), VarToken):
                            # This is a user-defined type
                            param_type = next(t).v
                        else:
                            raise ParseError("Expected parameter type")
                        raise ParseError("Expected parameter type")
                    param_token = next(t)
                    param_type = param_token.t + "[]" * param_token.array_dimensions if param_token.is_array else param_token.t
                    
                    params.append((param_name, param_type))
                    
                    # Parse additional parameters
                    while t.peek(None) == OperatorToken(','):
                        next(t)  # Consume comma
                        
                        if not isinstance(t.peek(None), VarToken):
                            raise ParseError("Expected parameter name after comma")
                        param_name = next(t).v
                        
                        expect(OperatorToken(":"))
                        if not isinstance(t.peek(None), TypeToken):
                            if isinstance(t.peek(None), VarToken):
                                # This is a user-defined type
                                param_type = next(t).v
                            else:
                                raise ParseError("Expected parameter type")
                            raise ParseError("Expected parameter type")
                        param_token = next(t)
                        param_type = param_token.t + "[]" * param_token.array_dimensions if param_token.is_array else param_token.t
                        
                        params.append((param_name, param_type))
                
                expect(OperatorToken(")"))

                # Handle return type - also allow user-defined types
                expect(OperatorToken(":"))
                if isinstance(t.peek(None), TypeToken):
                    return_type = next(t).t
                elif isinstance(t.peek(None), VarToken):
                    return_type = next(t).v
                else:
                    raise ParseError("Expected return type")

                expect(OperatorToken("{"))
                
                # Parse the function body statements
                body = parse_statements()
                
                expect(OperatorToken("}"))
                
                # Continue parsing after function definition
                if t.peek(None) is not None and not (isinstance(t.peek(), OperatorToken) and t.peek().o == '}'):
                    rest = parse_statements() 
                else:
                    rest = Sequence([])
                    
                return Fun(name, params, return_type, body, rest)
                
            case KeywordToken("dict"):
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError("Expected dictionary name")
                name = next(t).v
                expect(OperatorToken("="))
                expect(OperatorToken("{"))
                pairs = []
                while t.peek(None) != OperatorToken("}"):
                    key = parse_expr()
                    expect(OperatorToken(":"))
                    value = parse_expr()
                    pairs.append((key, value))
                    if t.peek(None) == OperatorToken(","):
                        next(t)
                expect(OperatorToken("}"))
                expect(OperatorToken(";"))
                # print(pairs)
                rest = parse_statements() if t.peek(None) is not None else body
                # print("rest",rest)
                return Let(name, Dict(pairs), rest)      
            case KeywordToken("if"):
                next(t)
                expect(OperatorToken("("))  # Expect opening parenthesis
                cond = parse_expr()
                expect(OperatorToken(")"))  # Expect closing parenthesis
                expect(OperatorToken("{"))  # Expect opening brace
                then = parse_statements()   # Parse statements inside braces
                expect(OperatorToken("}"))  # Expect closing brace

                if t.peek(None) == KeywordToken("else"):
                    next(t)
                    expect(OperatorToken("{"))
                    else_ = parse_statements()
                    expect(OperatorToken("}"))
                else:
                    else_ = Number("0")  # Default else case

                return If(cond, then, else_)
            case KeywordToken("return"):
                next(t)
                expr = parse_expr()
                if t.peek(None) == OperatorToken(";"):
                    next(t)
                return Return(expr)
            case KeywordToken("while"):
                next(t)
                expect(OperatorToken("("))  # Expect opening parenthesis
                cond = parse_expr()
                expect(OperatorToken(")"))  # Expect closing parenthesis
                expect(OperatorToken("{"))  # Expect opening brace
                body = parse_statements()   # Parse statements inside braces
                expect(OperatorToken("}"))  # Expect closing brace
                return While(cond, body)
            case KeywordToken("continue"):
                next(t)
                if t.peek(None) == OperatorToken(";"):
                    next(t)
                return Continue()
            case KeywordToken("break"):
                next(t)
                if t.peek(None) == OperatorToken(";"):
                    next(t)
                return Break()
            case KeywordToken("println"):
                next(t)
                expect(OperatorToken("("))
                expr = parse_expr()
                expect(OperatorToken(")"))
                expect(OperatorToken(";"))  # Always require semicolon
                return PrintLn(expr)
            case KeywordToken("type"):
                next(t)  # consume 'type'
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError("Expected type name")
                type_name = next(t).v
                
                # Register type name early so it can be used in field types
                if type_name not in user_defined_types:
                    user_defined_types[type_name] = {}
                
                # Expect opening brace
                expect(OperatorToken("{"))
                
                # Parse field definitions
                fields = {}
                while t.peek(None) != OperatorToken("}"):
                    # Parse field name (as string literal)
                    if not isinstance(t.peek(None), StringToken):
                        raise ParseError("Expected field name as string literal")
                    field_name = next(t).v
                    
                    # Expect colon
                    expect(OperatorToken(":"))
                    
                    # Parse field type - allow TypeToken or VarToken (for user-defined types)
                    if isinstance(t.peek(None), TypeToken):
                        field_type_token = next(t)
                        field_type = field_type_token.t + "[]" if field_type_token.is_array else field_type_token.t
                    elif isinstance(t.peek(None), VarToken):
                        # This is a user-defined type
                        field_type = next(t).v
                    else:
                        raise ParseError("Expected field type")
                    
                    # Add the field to our type definition
                    fields[field_name] = field_type
                    
                    # Parse comma or closing brace
                    if t.peek(None) == OperatorToken(","):
                        next(t)  # consume comma
                    # Don't check for closing brace here - let the while loop condition handle it
                
                # Replace the early registration with complete field set
                user_defined_types[type_name] = fields
                
                # Consume closing brace
                expect(OperatorToken("}"))
                expect(OperatorToken(";"))
                
                return TypeDef(type_name, fields)
            
            # Remove the old case for type instantiation as it will now be handled at the top
            
            case _:
                return parse_expr()
       

    def parse_expr():
        expr = parse_assign()
        # If the expression is a function call and we're at statement level,
        # expect a semicolon
        if isinstance(expr, Call) and isinstance(t.peek(None), OperatorToken) and t.peek().o == ';':
            next(t)
        return expr

    def parse_assign():
        if isinstance(t.peek(None), VarToken):
            var = next(t)
            if t.peek(None) == OperatorToken('='):
                next(t)
                expr = parse_expr()
                return Assign(var.v, expr)
            # Look for type instantiation as an expression
            elif var.v in user_defined_types and isinstance(t.peek(None), OperatorToken) and t.peek().o == '{':
                type_name = var.v
                # Parse instantiation body
                next(t)  # consume '{'
                pairs = []
                
                while t.peek(None) != OperatorToken("}"):
                    # Field key must be a string literal
                    if not isinstance(t.peek(None), StringToken):
                        raise ParseError("Expected field name as string literal")
                    key = String(next(t).v)
                    
                    expect(OperatorToken(":"))
                    value = parse_expr()  # This allows for recursive type instantiation
                    pairs.append((key, value))
                    
                    if t.peek(None) == OperatorToken(","):
                        next(t)
                        # Check if there's another field after comma
                        if t.peek(None) == OperatorToken("}"):
                            break
                
                expect(OperatorToken("}"))
                return TypeInstantiation(type_name, Dict(pairs))
            else:
                t.prepend(var)
        return parse_logical()

    def parse_logical():
        l = parse_comparison()
        while True:
            match t.peek(None):
                case KeywordToken(op) if op in {"and", "or"}:
                    next(t)
                    r = parse_comparison()
                    l = BinOp(op, l, r)
                case _:
                    return l

    def parse_comparison():
        l = parse_add()
        while True:  
            match t.peek(None):
                case OperatorToken(op) if op in {'<', '>', '<=', '>=', '==', '!='}:
                    operator = next(t).o
                    r = parse_add()
                    l = BinOp(operator, l, r)
                case _:
                    return l

    def parse_add():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken('+') | OperatorToken('-'):
                    op = next(t).o
                    ast = BinOp(op, ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_power()  
        while True:
            match t.peek(None):
                case OperatorToken('*') | OperatorToken('/') | OperatorToken('%'):  
                    op = next(t).o
                    ast = BinOp(op, ast, parse_power()) 
                case _:
                    return ast

    def parse_power():  
        ast = parse_concat()  
        while True:
            match t.peek(None):
                case OperatorToken('**'):
                    next(t)
                    ast = BinOp('**', ast, parse_concat())
                case _:
                    return ast

    def parse_concat():  
        ast = parse_atom()
        while True:
            match t.peek(None):
                case OperatorToken('++'):
                    next(t)
                    ast = BinOp('++', ast, parse_atom())
                case _:
                    return ast

    def parse_atom():
        # print(f"parse_atom: {t.peek(None)}")  # Debugging statement
        match t.peek(None):
            case OperatorToken('{'):
                next(t)  # consume opening brace
                expr = parse_statements()
                expect(OperatorToken("}"))  # expect closing brace
                return expr
            case TypeToken(typ):  # Changed from KeywordToken to TypeToken
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError(f"Expected variable name after {typ}")
                var = next(t).v
                expect(OperatorToken("="))
                expr = parse_expr()
                expect(OperatorToken(";"))
                # Create a sequence that continues evaluating after the declaration
                next_expr = parse_statements() if t.peek(None) is not None else Var(var)
                return Let(var, expr, next_expr)
            case KeywordToken("println"):
                next(t)
                expect(OperatorToken("("))
                expr = parse_expr()
                expect(OperatorToken(")"))
                expect(OperatorToken(";"))  # Always require semicolon
                return PrintLn(expr)
            case KeywordToken("str"):
                next(t)
                expect(OperatorToken("("))
                expr = parse_expr()
                expect(OperatorToken(")"))
                return StrConversion(expr)
            case ArrayToken(elements):
                next(t)
                return Array([Number(e.v) for e in elements])
            case VarToken(name):
                next(t)
                
                # First create the base variable expression
                expr = Var(name)
                
                # Now handle any possible chained operations like array access, function calls, 
                # or dictionary/field access
                while True:
                    if isinstance(t.peek(None), OperatorToken):
                        if t.peek().o == '[':  # Array access
                            indices = []
                            # First dimension
                            next(t)  # consume [
                            indices.append(parse_expr())
                            if isinstance(t.peek(None), OperatorToken) and t.peek().o == ':':
                                next(t)  # consume :
                                end = parse_expr()
                                expect(OperatorToken(']'))
                                expr = Slice(expr, indices[0], end)
                            else:
                                expect(OperatorToken(']'))
                                 # Additional dimensions if any
                                while isinstance(t.peek(None), OperatorToken) and t.peek().o == '[':
                                    next(t)  # consume [
                                    indices.append(parse_expr())
                                if isinstance(t.peek(None), OperatorToken) and t.peek().o == '=':
                                    next(t)  # consume =
                                    value = parse_expr()
                                    expr = ArrayAssign(expr, indices, value)
                                else:
                                    expr = ArrayAccess(expr, indices)
                        elif t.peek().o == '(':  # Function call
                            next(t)  # consume opening parenthesis
                            args = []
                            # Handle empty parameter list
                            if isinstance(t.peek(None), OperatorToken) and t.peek().o == ')':
                                next(t)  # consume closing parenthesis
                            else:
                                # Parse the first argument
                                args.append(parse_expr())
                                
                                # Parse additional arguments
                                while isinstance(t.peek(None), OperatorToken) and t.peek().o == ',':
                                    next(t)  # consume comma
                                    args.append(parse_expr())
                                
                                expect(OperatorToken(")"))
                            
                            return Call(name, args)
                        elif t.peek().o == '{':  # Dictionary/field access
                            next(t)  # consume {
                            key = parse_expr()
                            expect(OperatorToken('}'))
                            if isinstance(t.peek(None), OperatorToken) and t.peek().o == '=':
                                next(t)  # consume =
                                value = parse_expr()
                                expr = DictAssign(expr, key, value)
                                break  # Assignment ends the chain
                            else:
                                expr = DictAccess(expr, key)
                        else:
                            break  # No more chained operations
                    else:
                        break  # Not an operator, end of chain
                
                # Handle type instantiation (separate from chained access)
                if name in user_defined_types and expr == Var(name) and isinstance(t.peek(None), OperatorToken) and t.peek().o == '{':
                    # This is an inline type instantiation
                    type_name = name
                    expect(OperatorToken("{"))
                    pairs = []
                    
                    while t.peek(None) != OperatorToken("}"):
                        # Field key must be a string literal
                        if not isinstance(t.peek(None), StringToken):
                            raise ParseError("Expected field name as string literal")
                        key = String(next(t).v)
                        
                        expect(OperatorToken(":"))
                        value = parse_expr()  # This allows nested type instantiations
                        pairs.append((key, value))
                        
                        if t.peek(None) == OperatorToken(","):
                            next(t)
                            # Check if there's another field after comma
                            if t.peek(None) == OperatorToken("}"):
                                break
                    
                    expect(OperatorToken("}"))
                    return TypeInstantiation(type_name, Dict(pairs))
                
                return expr
            case OperatorToken('['):
                next(t)  # consume opening bracket
                elements = []
                
                # Handle empty array
                if isinstance(t.peek(None), OperatorToken) and t.peek().o == ']':
                    next(t)
                    return Array([])
                
                # Parse first element
                elements.append(parse_expr())
                
                # Parse remaining elements
                while isinstance(t.peek(None), OperatorToken) and t.peek().o == ',':
                    next(t)  # consume comma
                    elements.append(parse_expr())
                
                if not isinstance(t.peek(None), OperatorToken) or t.peek().o != ']':
                    raise ParseError("Expected ']' after array elements")
                next(t)  # consume closing bracket
                
                return Array(elements)
                
            # ...rest of parse_atom cases...
            case KeywordToken("len"):
                next(t)
                expect(OperatorToken("("))
                expr = parse_expr()
                expect(OperatorToken(")"))
                return Length(expr)
            case OperatorToken('('):
                next(t)
                expr = parse_expr()  
                if t.peek(None) != OperatorToken(')'):
                    raise ParseError("Expected closing bracket ')'")
                next(t)  
                return expr
            case NumberToken(v):
                next(t)
                return Number(v)
            case StringToken(v):
                next(t)
                return String(v)
            case _:
                raise ParseError(f"Unexpected token: {t.peek(None)}")

    return parse_statements()

# Add a new Bytecode class for compilation
@dataclass
class BytecodeInstruction:
    opcode: str
    args: list = None

class BytecodeCompiler:
    # Static variable to store the last compiled variables map
    last_variables = {}
    
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.variables = {}  # Maps variable names to indices
        self.global_vars = set()  # Track global variables
        self.labels = {}
        self.next_label = 0
        self.current_stack_size = 0
        self.max_stack_size = 0

    def get_label(self):
        """Generate a new unique label"""
        label = f"L{self.next_label}"
        self.next_label += 1
        return label

    def emit(self, opcode, *args):
        """Add an instruction to the bytecode sequence"""
        self.instructions.append(BytecodeInstruction(opcode, list(args)))
        
        # Update stack size tracking
        if opcode in ['LOAD_CONST', 'LOAD_VAR', 'LOAD_GLOBAL']:
            self.current_stack_size += 1
        elif opcode in ['STORE_VAR', 'STORE_GLOBAL', 'POP_TOP']:
            self.current_stack_size -= 1
        elif opcode in ['BINARY_ADD', 'BINARY_SUB', 'BINARY_MUL', 'BINARY_DIV',
                       'BINARY_MOD', 'BINARY_POWER', 'BINARY_CONCAT']:
            self.current_stack_size -= 1  # Two operands pop, one result push
        
        self.max_stack_size = max(self.max_stack_size, self.current_stack_size)
        
        return len(self.instructions) - 1

    def add_constant(self, value):
        """Add a constant to the constant pool"""
        if value not in self.constants:
            self.constants.append(value)
        return self.constants.index(value)
        
    def mark_as_global(self, var_name):
        """Mark a variable as global"""
        self.global_vars.add(var_name)
        
    def is_global(self, var_name):
        """Check if a variable is global"""
        return var_name in self.global_vars

    def compile(self, ast):
        """Compile an AST into bytecode"""
        # First pass: identify global variables
        self._identify_globals(ast)
        
        # Second pass: compile with knowledge of globals
        self._compile_node(ast)
        
        # Store the variables mapping for the VM to use
        BytecodeCompiler.last_variables = self.variables
        
        return {
            'instructions': self.instructions,
            'constants': self.constants,
            'variables': self.variables,
            'global_vars': self.global_vars,
            'max_stack': self.max_stack_size
        }
        
    def _identify_globals(self, node, scope=None):
        """First pass to identify global variables"""
        if scope is None:
            scope = set()  # Initialize empty scope for tracking local variables
            
        if node is None:
            return
            
        match node:
            case Let(var, expr, body, _):
                # Add variable to current scope
                if var not in scope:
                    self.global_vars.add(var)  # It's a global declaration
                    
                # Process the initializer expression
                self._identify_globals(expr, scope)
                
                # Create a new scope for the body that includes this variable
                new_scope = scope.copy()
                new_scope.add(var)
                self._identify_globals(body, new_scope)
                
            case Fun(n, params, rt, b, e):
                # Add function name to current scope
                if n not in scope:
                    self.global_vars.add(n)  # It's a global function
                    
                # Process function body with new scope including parameters
                func_scope = scope.copy()
                for param_name, _ in params:
                    func_scope.add(param_name)  # Parameters are local to function
                self._identify_globals(b, func_scope)
                
                # Continue with code after function
                self._identify_globals(e, scope)
                
            case Assign(name, expr):
                # Check if name is in scope
                if name not in scope:
                    self.global_vars.add(name)  # It's a global assignment
                self._identify_globals(expr, scope)
                
            case Var(name):
                # Nothing to do for variable references
                pass
                
            case BinOp(op, left, right):
                self._identify_globals(left, scope)
                self._identify_globals(right, scope)
                
            case If(cond, then, else_):
                self._identify_globals(cond, scope)
                self._identify_globals(then, scope)
                self._identify_globals(else_, scope)
                
            case Sequence(statements):
                for stmt in statements:
                    self._identify_globals(stmt, scope)
                    
            case While(cond, body):
                self._identify_globals(cond, scope)
                self._identify_globals(body, scope)
                
            case Call(n, args):
                for arg in args:
                    self._identify_globals(arg, scope)
                
            case Return(expr):
                self._identify_globals(expr, scope)
                
            # Handle other node types as needed
            case _:
                # For other node types, no specific action needed
                pass

    def _compile_node(self, node):
        """Recursively compile a node in the AST"""
        if node is None:
            return
            
        match node:
            case Number(val):
                const_idx = self.add_constant(int(val))
                self.emit("LOAD_CONST", const_idx)
            
            case String(val):
                const_idx = self.add_constant(val)
                self.emit("LOAD_CONST", const_idx)
            
            case BinOp(op, left, right):
                # Special handling for precedence in complex expressions
                if op == '*' and isinstance(left, BinOp) and left.op in ['+', '-']:
                    # First compute the right operand
                    self._compile_node(right)
                    # Then compute the left operand parts
                    self._compile_node(left.left)
                    self._compile_node(left.right)
                    # Apply the appropriate operations in the correct order
                    self.emit({'+': "BINARY_ADD", '-': "BINARY_SUB"}[left.op])
                    self.emit("BINARY_MUL")
                else:
                    # Normal compilation order for other expressions
                    self._compile_node(left)
                    self._compile_node(right)
                    
                    # Map operators to bytecode operations
                    op_map = {
                        "+": "BINARY_ADD",
                        "-": "BINARY_SUB",
                        "*": "BINARY_MUL",
                        "/": "BINARY_DIV",
                        "%": "BINARY_MOD",
                        "**": "BINARY_POWER",
                        "++": "BINARY_CONCAT",
                        "<": "BINARY_LT",
                        ">": "BINARY_GT",
                        "<=": "BINARY_LE",
                        ">=": "BINARY_GE",
                        "==": "BINARY_EQ",
                        "!=": "BINARY_NE",
                        "and": "BINARY_AND",
                        "or": "BINARY_OR"
                    }
                    self.emit(op_map[op])
            
            case Var(name):
                # Check if it's a global variable
                if self.is_global(name):
                    # Ensure it has an index
                    if name not in self.variables:
                        self.variables[name] = len(self.variables)
                    self.emit("LOAD_GLOBAL", self.variables[name])
                else:
                    # It's a local variable
                    if name not in self.variables:
                        self.variables[name] = len(self.variables)
                    self.emit("LOAD_VAR", self.variables[name])
            
            case Assign(name, expr):
                self._compile_node(expr)
                
                # Check if it's a global variable
                if self.is_global(name):
                    if name not in self.variables:
                        self.variables[name] = len(self.variables)
                    self.emit("STORE_GLOBAL", self.variables[name])
                else:
                    # It's a local variable
                    if name not in self.variables:
                        self.variables[name] = len(self.variables)
                    self.emit("STORE_VAR", self.variables[name])
            
            case Let(var, expr, body, _):
                self._compile_node(expr)
                if var not in self.variables:
                    self.variables[var] = len(self.variables)
                
                # Store in the correct context (local or global)
                if self.is_global(var):
                    self.emit("STORE_GLOBAL", self.variables[var])
                else:
                    self.emit("STORE_VAR", self.variables[var])
                
                self._compile_node(body)
            
            case If(cond, then, else_):
                else_label = self.get_label()
                end_label = self.get_label()
                
                # Compile condition
                self._compile_node(cond)
                self.emit("JUMP_IF_FALSE", else_label)
                
                # Compile then branch
                self._compile_node(then)
                self.emit("JUMP", end_label)
                
                # Compile else branch
                self.emit("LABEL", else_label)
                self._compile_node(else_)
                
                # End of if-else
                self.emit("LABEL", end_label)
            
            case While(cond, body):
                self._compile_while(node)
            
            case PrintLn(expr):
                self._compile_node(expr)
                self.emit("PRINT")
            
            case StrConversion(expr):
                self._compile_node(expr)
                self.emit("STR_CONVERT")
            
            case Sequence(statements):
                for i, stmt in enumerate(statements):
                    self._compile_node(stmt)
                    # Add POP_TOP if the statement produces a value that's not used
                    # and it's not the last statement in a sequence
                    if (i < len(statements) - 1 and 
                        not isinstance(stmt, (Assign, Let, If, While, PrintLn, TypeDef))):
                        self.emit("POP_TOP")
            
            case _:
                # Handle by the enhanced compile node
                enhanced_compile_node(self, node)

    def _compile_function(self, node):
        """Compile a function definition"""
        # Store function name in variables map
        if node.n not in self.variables:
            self.variables[node.n] = len(self.variables)
        
        # Generate unique labels for function entry and exit
        func_label = self.get_label()
        end_label = self.get_label()
        
        # Store function metadata in constants pool
        # (label, params, return_type)
        func_meta = (func_label, node.params, node.rt)
        func_meta_idx = self.add_constant(func_meta)
        
        # Create a function object and store it in the variable
        self.emit("LOAD_CONST", func_meta_idx)
        self.emit("MAKE_FUNCTION")
        self.emit("STORE_VAR", self.variables[node.n])
        
        # Jump over the function code
        self.emit("JUMP", end_label)
        
        # Function body starts here
        self.emit("LABEL", func_label)
        
        # Store the parameter values passed on the stack
        # These parameters will be pushed onto the stack by CALL_FUNCTION
        # Note: The parameters are already on the stack at this point, put there by CALL_FUNCTION
        for param_name, _ in reversed(node.params):
            if param_name not in self.variables:
                self.variables[param_name] = len(self.variables)
            self.emit("STORE_VAR", self.variables[param_name])
        
        # Compile the function body
        self._compile_node(node.b)
        
        # If no explicit return, add a default return None
        self.emit("LOAD_CONST", self.add_constant(0))  # Default return value
        self.emit("RETURN_VALUE")
        
        # Function definition is done, continue with the rest of the code
        self.emit("LABEL", end_label)
        
        # Compile the rest of the program
        self._compile_node(node.e)

    def _compile_call(self, node):
        """Compile a function call"""
        # Load the function object
        if node.n not in self.variables:
            self.variables[node.n] = len(self.variables)
        self.emit("LOAD_VAR", self.variables[node.n])
        
        # Evaluate and push arguments
        for arg in node.args:
            self._compile_node(arg)
        
        # Call the function
        self.emit("CALL_FUNCTION", len(node.args))  # Number of arguments

    def _compile_return(self, node):
        """Compile a return statement"""
        # Evaluate the return expression
        self._compile_node(node.expr)
        
        # Return from function
        self.emit("RETURN_VALUE")

# Define a BytecodeVM class to execute compiled bytecode
class BytecodeVM:
    def __init__(self, bytecode):
        self.instructions = bytecode['instructions']
        self.constants = bytecode['constants']
        # Initialize variables array with None values for all variables
        self.variables = [None] * max(len(bytecode['variables']) + 1, 1)
        # Store global variables set
        self.global_vars = bytecode['global_vars']
        # Create a separate globals dict for global variable access
        self.globals = {}
        # Built-in functions
        self.builtins = {'len': self._builtin_len}
        self.stack = []
        self.ip = 0  # Instruction pointer
        self.call_stack = []  # For function calls
        self.debug = False  # Debug mode flag
        # Add user-defined types dictionary
        self.user_defined_types = {}
    
    def _builtin_len(self, arg):
        """Built-in len function implementation"""
        if isinstance(arg, (list, str, dict)):
            return len(arg)
        else:
            raise TypeError(f"Object of type {type(arg).__name__} has no len()")
        
    def run(self):
        result = None
        try:
            while self.ip < len(self.instructions):
                instruction = self.instructions[self.ip]
                self.ip += 1
                
                opcode = instruction.opcode
                args = instruction.args if instruction.args else []
                
                if self.debug:
                    stack_str = str(self.stack)[-60:] if self.stack else "[]"
                    print(f"EXEC: {self.ip-1}: {opcode} {args} (Stack: {stack_str})")
                
                if opcode == "LOAD_CONST":
                    self.stack.append(self.constants[args[0]])
                
                elif opcode == "LOAD_VAR":
                    var_idx = args[0]
                    var_name = self._get_var_name(var_idx)
                    
                    # Check for built-in functions first
                    if var_name in self.builtins:
                        # For built-ins, we create a special callable object
                        self.stack.append(('__builtin__', var_name))
                        continue
                    
                    # For regular variables, we use the local vars first then fallback to globals
                    if var_idx >= len(self.variables) or self.variables[var_idx] is None:
                        # Check if it's a global variable
                        if var_name in self.globals:
                            self.stack.append(self.globals[var_name])
                        else:
                            raise ValueError(f"Variable at index {var_idx} not initialized")
                    else:
                        self.stack.append(self.variables[var_idx])
                
                elif opcode == "LOAD_GLOBAL":
                    var_idx = args[0]
                    var_name = self._get_var_name(var_idx)
                    # For global variables, we directly look in the globals dictionary
                    if var_name in self.globals:
                        self.stack.append(self.globals[var_name])
                    else:
                        raise ValueError(f"Global variable {var_name} not initialized")
                
                elif opcode == "STORE_VAR":
                    var_idx = args[0]
                    var_name = self._get_var_name(var_idx)
                    value = self.stack.pop()
                    
                    # Expand variables array if needed
                    if var_idx >= len(self.variables):
                        self.variables.extend([None] * (var_idx - len(self.variables) + 1))
                    
                    # Store in the local variables array
                    self.variables[var_idx] = value
                    
                    # If on the top frame and it's a global, also store in globals
                    if not self.call_stack and var_name in self.global_vars:
                        self.globals[var_name] = value
                
                elif opcode == "STORE_GLOBAL":
                    var_idx = args[0]
                    var_name = self._get_var_name(var_idx)
                    value = self.stack.pop()
                    
                    # Store in both the globals dict and the variables array
                    self.globals[var_name] = value
                    
                    if var_idx >= len(self.variables):
                        self.variables.extend([None] * (var_idx - len(self.variables) + 1))
                    self.variables[var_idx] = value
                
                elif opcode == "BINARY_ADD":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left + right)
                
                elif opcode == "BINARY_SUB":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left - right)
                
                elif opcode == "BINARY_MUL":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left * right)
                
                elif opcode == "BINARY_DIV":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left // right)
                
                elif opcode == "BINARY_MOD":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left % right)
                
                elif opcode == "BINARY_POWER":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left ** right)
                
                elif opcode == "BINARY_CONCAT":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    # String concatenation with type checking
                    if not isinstance(left, str) or not isinstance(right, str):
                        raise TypeError(f"Cannot concatenate {type(left).__name__} with {type(right).__name__}")
                    self.stack.append(left + right)
                
                elif opcode == "BINARY_LT":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left < right)
                
                elif opcode == "BINARY_GT":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left > right)
                
                elif opcode == "BINARY_LE":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left <= right)
                
                elif opcode == "BINARY_GE":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left >= right)
                
                elif opcode == "BINARY_EQ":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left == right)
                
                elif opcode == "BINARY_NE":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left != right)
                
                elif opcode == "BINARY_AND":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left and right)
                
                elif opcode == "BINARY_OR":
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left or right)
                
                elif opcode == "STR_CONVERT":
                    value = self.stack.pop()
                    self.stack.append(str(value))
                
                elif opcode == "PRINT":
                    if not self.stack:
                        print("ERROR: Stack underflow in PRINT operation")
                        continue
                    value = self.stack.pop()
                    print(value, flush=True)
                    result = value
                
                elif opcode == "POP_TOP":
                    self.stack.pop()
                
                elif opcode == "JUMP":
                    # Find the label index before updating IP
                    label_idx = self._find_label(args[0])
                    self.ip = label_idx
                
                elif opcode == "JUMP_IF_FALSE":
                    condition = self.stack.pop()
                    if not condition:
                        # Find the label index before updating IP
                        label_idx = self._find_label(args[0])
                        self.ip = label_idx
                
                elif opcode == "LABEL":
                    # Labels are just markers, no operation needed
                    pass
                
                elif opcode == "LOAD_ARRAY_ITEM":
                    idx = self.stack.pop()
                    arr = self.stack.pop()
                    if not isinstance(arr, (list, str)):
                        raise TypeError(f"Cannot index into {type(arr).__name__}")
                    if not isinstance(idx, int):
                        raise TypeError("Array index must be integer")
                    if idx < 0 or idx >= len(arr):
                        raise IndexError("Array index out of bounds")
                    self.stack.append(arr[idx])
                
                elif opcode == "STORE_ARRAY_ITEM":
                    value = self.stack.pop()
                    idx = self.stack.pop()
                    arr = self.stack.pop()
                    if not isinstance(arr, list):
                        raise TypeError(f"Cannot assign to {type(arr).__name__}")
                    if not isinstance(idx, int):
                        raise TypeError("Array index must be integer")
                    if idx < 0 or idx >= len(arr):
                        raise IndexError("Array index out of bounds")
                    arr[idx] = value
                    self.stack.append(value)
                
                elif opcode == "CREATE_ARRAY":
                    size = args[0]
                    elements = []
                    for _ in range(size):
                        elements.insert(0, self.stack.pop())
                    self.stack.append(elements)
                
                elif opcode == "GET_LENGTH":
                    # Pop the object whose length we need to get
                    obj = self.stack.pop()
                    
                    # Check the type and get its length
                    if isinstance(obj, (list, str, dict)):
                        length = len(obj)
                        self.stack.append(length)
                    else:
                        raise TypeError(f"Cannot get length of {type(obj).__name__}")
                
                elif opcode == "SLICE":
                    end_idx = self.stack.pop()
                    start_idx = self.stack.pop()
                    seq = self.stack.pop()
                    if not isinstance(seq, (list, str)):
                        raise TypeError(f"Cannot slice {type(seq).__name__}")
                    self.stack.append(seq[start_idx:end_idx])
                
                elif opcode == "CREATE_DICT":
                    size = args[0]
                    dict_obj = {}
                    # Pop pairs in reverse order (since later items are deeper in the stack)
                    for _ in range(size):
                        value = self.stack.pop()
                        key = self.stack.pop()
                        dict_obj[key] = value
                    self.stack.append(dict_obj)

                elif opcode == "LOAD_DICT_ITEM":
                    key = self.stack.pop()
                    dict_obj = self.stack.pop()
                    if not isinstance(dict_obj, dict):
                        raise TypeError(f"Cannot access key in non-dict type {type(dict_obj).__name__}")
                    try:
                        # Get the value for this key
                        value = dict_obj[key]
                        
                        # Push the value onto the stack
                        self.stack.append(value)
                        
                        # If this is a nested access, let the next instruction handle it
                        # The value is already on the stack
                    except KeyError:
                        raise KeyError(f"Key {key} not found in dictionary or object")

                elif opcode == "STORE_DICT_ITEM":
                    value = self.stack.pop()
                    key = self.stack.pop()
                    dict_obj = self.stack.pop()
                    if not isinstance(dict_obj, dict):
                        raise TypeError(f"Cannot assign key in non-dict type {type(dict_obj).__name__}")
                    dict_obj[key] = value
                    self.stack.append(value)
                
                elif opcode == "MAKE_FUNCTION":
                    # Function metadata is already on the stack
                    # Just keep it there (it's a tuple with function info)
                    pass
                    
                elif opcode == "CREATE_TYPE_DEF":
                    # Get type definition from arguments
                    type_name = args[0]
                    field_count = args[1]
                    
                    # Pop field definitions from stack (name, type pairs)
                    fields = {}
                    for _ in range(field_count):
                        field_type = self.stack.pop()  # Type comes second on stack
                        field_name = self.stack.pop()  # Name comes first on stack
                        fields[field_name] = field_type
                    
                    # Register the type
                    self.user_defined_types[type_name] = fields
                    
                    # Don't push anything onto the stack
                    # Type definitions don't have a runtime value
                
                elif opcode == "CREATE_TYPE_INSTANCE":
                    # Get type name from arguments
                    type_name = args[0]
                    
                    # Get instance fields from the Dict already on stack
                    fields_dict = self.stack.pop()
                    
                    if type_name not in self.user_defined_types:
                        raise TypeError(f"Unknown type: {type_name}")
                    
                    type_def = self.user_defined_types[type_name]
                    instance = {}
                    
                    # Check for required fields
                    for field_name in type_def:
                        if field_name not in fields_dict:
                            raise TypeError(f"Missing required field '{field_name}' for type {type_name}")
                    
                    # Check for extra fields
                    for field_name in fields_dict:
                        if field_name not in type_def:
                            raise TypeError(f"Unknown field '{field_name}' for type {type_name}")
                    
                    # Copy the fields to the instance
                    # We could do type checking here but we'll keep it simple
                    instance.update(fields_dict)
                    
                    # Push instance onto stack
                    self.stack.append(instance)
                
                elif opcode == "CALL_FUNCTION":
                    num_args = args[0]
                    # Pop arguments in reverse order
                    arg_vals = [self.stack.pop() for _ in range(num_args)]
                    arg_vals.reverse()  # Reverse to get correct argument order

                    # Pop function object (metadata tuple or built-in)
                    func_obj = self.stack.pop()

                    # Handle built-in functions
                    if isinstance(func_obj, tuple) and func_obj[0] == '__builtin__':
                        builtin_name = func_obj[1]
                        if builtin_name in self.builtins:
                            # Call the built-in function
                            if len(arg_vals) != 1:
                                raise TypeError(f"{builtin_name}() takes exactly 1 argument ({len(arg_vals)} given)")
                            result = self.builtins[builtin_name](arg_vals[0])
                            self.stack.append(result)
                            continue
                        else:
                            raise ValueError(f"Unknown built-in function: {builtin_name}")

                    # Handle regular functions
                    if not isinstance(func_obj, tuple) or len(func_obj) not in [3, 4]:
                        raise TypeError(f"Cannot call {func_obj}")

                    # Unpack function metadata
                    func_label, params, return_type = func_obj

                    # Check that number of arguments matches number of parameters
                    if len(arg_vals) != len(params):
                        raise TypeError(f"Function expected {len(params)} arguments but got {len(arg_vals)}")

                    # Save current instruction pointer for return
                    return_ip = self.ip

                    # Create a new variables array for the function call
                    # This preserves lexical scoping - local variables don't affect parent scope
                    new_vars = [None] * len(self.variables)

                    # Save current context to call stack (to restore on return)
                    self.call_stack.append((return_ip, self.variables))

                    # Set the new variables array as active
                    self.variables = new_vars

                    # Push arguments onto the stack for the function body to access
                    for arg_val in arg_vals:
                        self.stack.append(arg_val)

                    # Jump to function body
                    self.ip = self._find_label(func_label)

                elif opcode == "RETURN_VALUE":
                    # Get return value
                    return_value = self.stack.pop()

                    # Restore calling context if there's a saved context
                    if self.call_stack:
                        # Pop the last call frame
                        return_ip, saved_variables = self.call_stack.pop()

                        # Restore variables from before the call
                        self.variables = saved_variables

                        # Jump back to caller
                        self.ip = return_ip

                        # Push return value onto stack for caller
                        self.stack.append(return_value)
                    else:
                        # Top-level return or end of program
                        self.stack.append(return_value)
                        self.ip = len(self.instructions)  # Exit execution
                
                else:
                    raise ValueError(f"Unknown opcode: {opcode}")
            
            # Return the last value on the stack, if any
            return result if not self.stack else self.stack[-1]
                
        except Exception as e:
            print(f"VM Error at instruction {self.ip-1}: {opcode} {args}")
            print(f"Stack: {self.stack}")
            print(f"Variables: {self.variables}")
            raise
            
    def _find_label(self, label):
        """Find the index of a label in the instruction sequence"""
        for i, instr in enumerate(self.instructions):
            if instr.opcode == "LABEL" and instr.args[0] == label:
                return i
        raise ValueError(f"Label not found: {label}")
        
    def _get_var_name(self, var_idx):
        """Get variable name from index (reverse lookup in variables map)"""
        for name, idx in BytecodeCompiler.last_variables.items():
            if idx == var_idx:
                return name
        return f"var{var_idx}"  # Fallback if name not found

# Add additional bytecode-related methods to compiler
def _compile_array(self, node):
    """Compile array creation"""
    for element in node.elements:
        self._compile_node(element)
    self.emit("CREATE_ARRAY", len(node.elements))

def _compile_array_access(self, node):
    """Compile array access expression with support for multi-dimensional arrays"""
    # First load the base array
    self._compile_node(node.array)
    
    # For each dimension, load the index and access the array
    for i, index in enumerate(node.indices):
        self._compile_node(index)
        self.emit("LOAD_ARRAY_ITEM")
        # No need for additional handling after loading the last dimension

def _compile_array_assign(self, node):
    """Compile array element assignment with support for multi-dimensional arrays"""
    # First load the base array
    self._compile_node(node.array)
    
    # For each dimension except the last, load the index and access the array
    for i, index in enumerate(node.indices[:-1]):
        self._compile_node(index)
        self.emit("LOAD_ARRAY_ITEM")
    
    # For the last dimension, we'll use STORE_ARRAY_ITEM
    self._compile_node(node.indices[-1])
    self._compile_node(node.value)
    self.emit("STORE_ARRAY_ITEM")

def _compile_length(self, node):
    """Compile length function call"""
    self._compile_node(node.expr)
    self.emit("GET_LENGTH")

def _compile_slice(self, node):
    """Compile array slicing"""
    self._compile_node(node.sequence)
    self._compile_node(node.start)
    self._compile_node(node.end)
    self.emit("SLICE")

BytecodeCompiler._compile_slice = _compile_slice

# Update the BytecodeCompiler._compile_node method to handle these node types
BytecodeCompiler._compile_array = _compile_array
BytecodeCompiler._compile_array_access = _compile_array_access
BytecodeCompiler._compile_array_assign = _compile_array_assign
BytecodeCompiler._compile_length = _compile_length

# Add these cases to the _compile_node method's match statement
def _compile_function(self, node):
    """Compile a function definition"""
    # Store function name in variables map
    if node.n not in self.variables:
        self.variables[node.n] = len(self.variables)
    
    # Generate unique labels for function entry and exit
    func_label = self.get_label()
    end_label = self.get_label()
    
    # Store function metadata in constants pool
    # (label, params, return_type)
    func_meta = (func_label, node.params, node.rt)
    func_meta_idx = self.add_constant(func_meta)
    
    # Create a function object and store it in the variable
    self.emit("LOAD_CONST", func_meta_idx)
    self.emit("MAKE_FUNCTION")
    self.emit("STORE_VAR", self.variables[node.n])
    
    # Jump over the function code
    self.emit("JUMP", end_label)
    
    # Function body starts here
    self.emit("LABEL", func_label)
    
    # Store the parameter values passed on the stack
    # These parameters will be pushed onto the stack by CALL_FUNCTION
    # Note: The parameters are already on the stack at this point, put there by CALL_FUNCTION
    for param_name, _ in reversed(node.params):
        if param_name not in self.variables:
            self.variables[param_name] = len(self.variables)
        self.emit("STORE_VAR", self.variables[param_name])
    
    # Compile the function body
    self._compile_node(node.b)
    
    # If no explicit return, add a default return None
    self.emit("LOAD_CONST", self.add_constant(0))  # Default return value
    self.emit("RETURN_VALUE")
    
    # Function definition is done, continue with the rest of the code
    self.emit("LABEL", end_label)
    
    # Compile the rest of the program
    self._compile_node(node.e)

def _compile_call(self, node):
    """Compile a function call"""
    # Load the function object
    if node.n not in self.variables:
        self.variables[node.n] = len(self.variables)
    self.emit("LOAD_VAR", self.variables[node.n])
    
    # Evaluate and push arguments
    for arg in node.args:
        self._compile_node(arg)
    
    # Call the function
    self.emit("CALL_FUNCTION", len(node.args))  # Number of arguments

def _compile_return(self, node):
    """Compile a return statement"""
    # Evaluate the return expression
    self._compile_node(node.expr)
    
    # Return from function
    self.emit("RETURN_VALUE")

# Assign these methods to the BytecodeCompiler class
BytecodeCompiler._compile_function = _compile_function
BytecodeCompiler._compile_call = _compile_call
BytecodeCompiler._compile_return = _compile_return

# Add dictionary compilation support methods to BytecodeCompiler
def _compile_dict(self, node):
    """Compile dictionary creation"""
    # Compile each key-value pair
    for key, value in node.pairs:
        self._compile_node(key)
        self._compile_node(value)
    self.emit("CREATE_DICT", len(node.pairs))

def _compile_dict_access(self, node):
    """Compile dictionary access"""
    self._compile_node(node.dict)
    self._compile_node(node.key)
    self.emit("LOAD_DICT_ITEM")

def _compile_dict_assign(self, node):
    """Compile dictionary assignment"""
    self._compile_node(node.dict)
    self._compile_node(node.key)
    self._compile_node(node.value)
    self.emit("STORE_DICT_ITEM")

# Assign these methods to the BytecodeCompiler class
BytecodeCompiler._compile_dict = _compile_dict
BytecodeCompiler._compile_dict_access = _compile_dict_access
BytecodeCompiler._compile_dict_assign = _compile_dict_assign

# Then update the _compile_node method to use these methods
original_compile_node = BytecodeCompiler._compile_node

def enhanced_compile_node(self, node):
    if node is None:
        return
    
    match node:
        case Array(elements):
            self._compile_array(node)
        case ArrayAccess(array, indices):
            self._compile_array_access(node)
        case ArrayAssign(array, indices, value):
            self._compile_array_assign(node)
        case Length(expr):
            self._compile_length(node)
        case Slice(sequence, start, end):
            self._compile_slice(node)
        case Fun(n, params, rt, b, e):
            self._compile_function(node)
        case Call(n, args):
            self._compile_call(node)
        case Return(expr):
            self._compile_return(node)
        case Dict(pairs):
            self._compile_dict(node)
        case DictAccess(dict, key):
            self._compile_dict_access(node)
        case DictAssign(dict, key, value):
            self._compile_dict_assign(node)
        case Break():
            self._compile_break(node)
        case TypeDef(name, fields):
            self._compile_type_def(node)
        case TypeInstantiation(type_name, fields):
            self._compile_type_instantiation(node)
        case _:
            original_compile_node(self, node)

# Now we can safely update the _compile_node method
BytecodeCompiler._compile_node = enhanced_compile_node

# Add compilation function to our interpreter
def compile_and_run(ast, env=None):
    """Compile AST to bytecode and run it with the VM"""
    compiler = BytecodeCompiler()
    bytecode = compiler.compile(ast)
    
    # Initialize variables from environment
    if env:
        for var_name, value in env:
            if var_name in compiler.variables:
                var_idx = compiler.variables[var_name]
                # Initialize VM variables
                while len(bytecode['variables']) <= var_idx:
                    bytecode['variables'][var_idx] = None
                bytecode['variables'][var_idx] = value
    
    vm = BytecodeVM(bytecode)
    return vm.run()

# Add break compilation support method to BytecodeCompiler
def _compile_break(self, node):
    """Compile a break statement"""
    # Get the innermost loop's end label
    if not hasattr(self, 'loop_end_labels') or not self.loop_end_labels:
        raise SyntaxError("Break statement outside of loop")
    end_label = self.loop_end_labels[-1]
    self.emit("JUMP", end_label)

# Add to the BytecodeCompiler class
BytecodeCompiler._compile_break = _compile_break

def _compile_while(self, node):
    """Compile while loop with support for break statements"""
    # Create labels for loop start and end
    start_label = self.get_label()
    end_label = self.get_label()
    
    # Initialize loop_end_labels if it doesn't exist
    if not hasattr(self, 'loop_end_labels'):
        self.loop_end_labels = []
    
    # Push the end label onto the stack for break statements
    self.loop_end_labels.append(end_label)
    
    # Emit loop start label
    self.emit("LABEL", start_label)
    
    # Compile condition
    self._compile_node(node.cond)
    
    # Jump to end if condition is false
    self.emit("JUMP_IF_FALSE", end_label)
    
    # Compile loop body
    self._compile_node(node.body)
    
    # Jump back to start
    self.emit("JUMP", start_label)
    
    # Emit loop end label
    self.emit("LABEL", end_label)
    
    # Pop the end label as we're leaving the loop
    self.loop_end_labels.pop()

# Add this method to the BytecodeCompiler class
BytecodeCompiler._compile_while = _compile_while

def compile_with_static_type_check(code_string):
    """
    Parse, statically type check, and compile code.
    Returns the bytecode or raises TypeCheckError if type check fails.
    """
    # Parse code to AST
    ast = parse(code_string)
    
    # Perform static type checking
    type_checker = TypeChecker()
    try:
        type_checker.check(ast)
        print("Static type check passed!")
    except TypeCheckError as e:
        print(f"Type error: {e}")
        raise
    
    # If type check passes, compile to bytecode
    compiler = BytecodeCompiler()
    bytecode = compiler.compile(ast)
    
    return bytecode

# Add type definition and instantiation compilation methods to BytecodeCompiler
def _compile_type_def(self, node):
    """Compile a type definition"""
    # Store the type name as a constant
    type_name = node.name
    
    # Push each field name and type onto stack in reverse order
    # (since we'll pop them in reverse when creating the type)
    fields = list(node.fields.items())
    for field_name, field_type in fields:
        # Add constants for the field name and type
        name_idx = self.add_constant(field_name)
        type_idx = self.add_constant(field_type)
        
        # Push them onto the stack
        self.emit("LOAD_CONST", name_idx)
        self.emit("LOAD_CONST", type_idx)
    
    # Create the type definition
    self.emit("CREATE_TYPE_DEF", type_name, len(fields))
    
    # Since type definitions don't push anything onto the stack,
    # we don't need to pop anything
    # Remove the POP_TOP instruction

def _compile_type_instantiation(self, node):
    """Compile a type instantiation"""
    # First compile the fields dictionary
    self._compile_node(node.fields)
    
    # Then create an instance of the type
    self.emit("CREATE_TYPE_INSTANCE", node.type_name)

# Assign these methods to the BytecodeCompiler class
BytecodeCompiler._compile_type_def = _compile_type_def
BytecodeCompiler._compile_type_instantiation = _compile_type_instantiation