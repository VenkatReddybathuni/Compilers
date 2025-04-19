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
    a: str       # argument name
    at: str      # argument type
    rt: str      # return type
    b: AST       # body
    e: AST       # expression

@dataclass
class Call(AST):
    n: str    
    a: AST    

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
    index: AST

@dataclass
class ArrayAssign(AST):
    array: AST
    index: AST
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

@dataclass
class ArrayToken(Token):
    elements: list[Token]

@dataclass
class Slice(AST):
    sequence: AST
    start: AST
    end: AST

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
        return ("x", "any", Length(Var("x")), "int")
    env_reversed = reversed(env)
    for u, uv in env_reversed:
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
def e(tree: AST, env=None) -> int | bool | str | list:
    if env is None:
        env = []  # Empty list for environment

    match tree:
        case PrintLn(expr):
            result = e(expr, env)
            print(result)
            return result
        case Number(v):
            return int(v)
        case Var(v):
            return lookup(env, v)
        case Fun(f, a, at, rt, b, c):
            # Store function definition with its type information
            env.append((f, (a, at, b, rt)))  # Store param name, param type, body, return type
            return e(c, env)
        case Call(f, x):
            param, param_type, body, return_type = lookup(env, f)  # Get function definition with types
            arg_value = e(x, env)

            # Add explicit conversion for string parameters if needed
            if param_type == "string" and isinstance(arg_value, int):
                arg_value = str(arg_value)
            elif param_type == "int" and isinstance(arg_value, str):
                raise TypeError(f"Function '{f}' expects int but got string")

            try:
                check_type(arg_value, param_type)
            except TypeError as te:
                raise TypeError(f"Function '{f}' parameter type mismatch: {str(te)}")

            # Create function environment with access to outer scope
            call_env = env.copy()  # Copy the outer environment to allow access to global vars
            
            # Add parameter binding - this will shadow any existing variable with same name
            update_env(call_env, param, arg_value)
            
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
            # print(var)
            # print("expression",expr)
            value = e(expr, env)  
            # print("value",value)
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
        case ArrayAccess(array, index):
            arr = e(array, env)
            idx = e(index, env)
            if isinstance(arr, (list, str)):
                if 0 <= idx < len(arr):
                    return arr[idx]
                raise IndexError("Array index out of bounds")
            raise TypeError(f"Cannot index into {type(arr).__name__}")
        case ArrayAssign(array, index, value):
            arr = e(array, env)
            idx = e(index, env)
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

            if not isinstance(idx, int):
                raise TypeError("Array index must be integer")
            if isinstance(arr, list):
                if 0 <= idx < len(arr):
                    arr[idx] = val
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
            # print(d)
            # print(f"Accessing key '{k}' in dict: {d}")
            # if not isinstance(d, dict):
            #     raise TypeError(f"Cannot access key in non-dict type {type(d).__name__}")
            # print(f"Accessing key '{k}' in dict: {d}")
            return d[k]
        case DictAssign(dict, key, value):
            d = e(dict, env)
            k = e(key, env)
            v = e(value, env)
            # if not isinstance(d, dict):
            #     raise TypeError(f"Cannot assign key in non-dict type {type(d).__name__}")
            d[k] = v
            return v

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
            while i < len(s) and (s[i].isalpha() or s[i].isdigit()):  # Allow digits in identifiers
                t = t + s[i]
                i = i + 1
            # print(t)
            # Check if this is an array type (e.g. "int[]")
            is_array = False
            if i + 1 < len(s) and s[i] == '[' and s[i + 1] == ']':
                is_array = True
                i += 2
                
            if t in {"and", "or", "if", "else", "fun", "return", "println", "str", "while", "continue", "break", "dict"}:  # Added while, continue, break
                yield KeywordToken(t)
            elif t in {"int", "float", "string", "void", "bool"}:  # Types are now handled separately
                yield TypeToken(t, is_array)
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

class ParseError(Exception):
    pass

def parse(s: str) -> AST:
    from more_itertools import peekable
    tokens = list(lex(s))
    # print(tokens)
    t = peekable(tokens)
    # print(lex(s))
    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError(f"Expected {what}")  

    def parse_statements():
        statements = []
        while t.peek(None) is not None:
            if isinstance(t.peek(), OperatorToken) and t.peek().o == '}':
                break

            stmt = parse_stmt()
            # print(stmt)
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
            case TypeToken(typ, is_array):
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError(f"Expected variable name after {typ}")
                var = next(t).v
                var_type = f"{typ}[]" if is_array else typ
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
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError("Expected function name")
                name = next(t).v
                expect(OperatorToken("("))

                # Parse parameter name
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError("Expected parameter name")
                param = next(t).v

                # Parse parameter type
                expect(OperatorToken(":"))
                if not isinstance(t.peek(None), TypeToken):
                    raise ParseError("Expected parameter type")
                param_token = next(t)
                param_type = param_token.t + "[]" if param_token.is_array else param_token.t

                expect(OperatorToken(")"))

                # Handle return type
                expect(OperatorToken(":"))
                if not isinstance(t.peek(None), TypeToken):
                    raise ParseError("Expected return type")
                return_type = next(t).t

                expect(OperatorToken("{"))
                body = parse_statements()
                expect(OperatorToken("}"))
                # Continue parsing after function definition
                rest = parse_statements() if t.peek(None) is not None else body
                return Fun(name, param, param_type, return_type, body, rest)
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
                if isinstance(t.peek(None), OperatorToken) and t.peek().o == '[':
                    next(t)  # consume [
                    index = parse_expr()
                    if isinstance(t.peek(None), OperatorToken) and t.peek().o == ':':
                        next(t)  # consume :
                        end = parse_expr()
                        expect(OperatorToken(']'))
                        return Slice(Var(name), index, end)
                    expect(OperatorToken(']'))
                    if isinstance(t.peek(None), OperatorToken) and t.peek().o == '=':
                        next(t)  # consume =
                        value = parse_expr()
                        return ArrayAssign(Var(name), index, value)
                    return ArrayAccess(Var(name), index)
                elif isinstance(t.peek(None), OperatorToken) and t.peek().o == '(':
                    next(t)
                    arg = parse_expr()
                    expect(OperatorToken(")"))
                    return Call(name, arg)
                elif isinstance(t.peek(None), OperatorToken) and t.peek().o == '{':
                    next(t)  # consume {
                    key = parse_expr()
                    expect(OperatorToken('}'))
                    if isinstance(t.peek(None), OperatorToken) and t.peek().o == '=':
                        next(t)  # consume =
                        value = parse_expr()
                        return DictAssign(Var(name), key, value)
                    return DictAccess(Var(name), key)
                return Var(name)
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

    return parse_stmt()

# Add a new Bytecode class for compilation
@dataclass
class BytecodeInstruction:
    opcode: str
    args: list = None

class BytecodeCompiler:
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.variables = {}
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
        elif opcode in ['STORE_VAR', 'POP_TOP']:
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

    def compile(self, ast):
        """Compile an AST into bytecode"""
        self._compile_node(ast)
        return {
            'instructions': self.instructions,
            'constants': self.constants,
            'variables': self.variables,
            'max_stack': self.max_stack_size
        }

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
                if name not in self.variables:
                    self.variables[name] = len(self.variables)
                self.emit("LOAD_VAR", self.variables[name])
            
            case Assign(name, expr):
                self._compile_node(expr)
                if name not in self.variables:
                    self.variables[name] = len(self.variables)
                self.emit("STORE_VAR", self.variables[name])
            
            case Let(var, expr, body, _):
                self._compile_node(expr)
                if var not in self.variables:
                    self.variables[var] = len(self.variables)
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
                start_label = self.get_label()
                end_label = self.get_label()
                
                self.emit("LABEL", start_label)
                self._compile_node(cond)
                self.emit("JUMP_IF_FALSE", end_label)
                self._compile_node(body)
                self.emit("JUMP", start_label)
                self.emit("LABEL", end_label)
            
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
                    if i < len(statements) - 1 and not isinstance(stmt, (Assign, Let, If, While, PrintLn)):
                        self.emit("POP_TOP")
            
            case _:
                raise NotImplementedError(f"Bytecode compilation not implemented for {type(node)}")

    def _compile_function(self, node):
        """Compile a function definition"""
        # Store function name in variables map
        if node.n not in self.variables:
            self.variables[node.n] = len(self.variables)
        
        # Generate unique labels for function entry and exit
        func_label = self.get_label()
        end_label = self.get_label()
        
        # Store function metadata in constants pool
        # (label, param_name, return_type)
        func_meta = (func_label, node.a, node.rt)
        func_meta_idx = self.add_constant(func_meta)
        
        # Create a function object and store it in the variable
        self.emit("LOAD_CONST", func_meta_idx)
        self.emit("MAKE_FUNCTION")
        self.emit("STORE_VAR", self.variables[node.n])
        
        # Jump over the function code
        self.emit("JUMP", end_label)
        
        # Function body starts here
        self.emit("LABEL", func_label)
        
        # Add parameter to variables
        if node.a not in self.variables:
            self.variables[node.a] = len(self.variables)
        
        # Store the parameter value passed on the stack
        self.emit("STORE_VAR", self.variables[node.a])
        
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
        
        # Evaluate and push argument
        self._compile_node(node.a)
        
        # Call the function
        self.emit("CALL_FUNCTION", 1)  # 1 argument

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
        self.variables = [None] * max(len(bytecode['variables']), 1)
        self.stack = []
        self.ip = 0  # Instruction pointer
        self.call_stack = []  # For function calls
        
    def run(self):
        result = None
        try:
            while self.ip < len(self.instructions):
                instruction = self.instructions[self.ip]
                self.ip += 1
                
                opcode = instruction.opcode
                args = instruction.args if instruction.args else []
                
                if opcode == "LOAD_CONST":
                    self.stack.append(self.constants[args[0]])
                
                elif opcode == "LOAD_VAR":
                    var_idx = args[0]
                    if var_idx >= len(self.variables) or self.variables[var_idx] is None:
                        raise ValueError(f"Variable at index {var_idx} not initialized")
                    self.stack.append(self.variables[var_idx])
                
                elif opcode == "STORE_VAR":
                    var_idx = args[0]
                    if var_idx >= len(self.variables):
                        # Expand variables array if needed
                        self.variables.extend([None] * (var_idx - len(self.variables) + 1))
                    self.variables[var_idx] = self.stack.pop()
                
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
                    value = self.stack.pop()
                    print(value)
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
                    obj = self.stack.pop()
                    if not isinstance(obj, (list, str)):
                        raise TypeError(f"Cannot get length of {type(obj).__name__}")
                    self.stack.append(len(obj))
                
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
                        self.stack.append(dict_obj[key])
                    except KeyError:
                        raise KeyError(f"Key {key} not found in dictionary")

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

                elif opcode == "CALL_FUNCTION":
                    num_args = args[0]
                    # Pop arguments (we only support 1 arg for now)
                    arg_val = self.stack.pop()
                    
                    # Pop function object (metadata tuple)
                    func_obj = self.stack.pop()
                    
                    if not isinstance(func_obj, tuple) or len(func_obj) != 3:
                        raise TypeError(f"Cannot call {func_obj}")
                    
                    # Unpack function metadata
                    func_label, param_name, return_type = func_obj
                    
                    # Save current instruction pointer for return
                    return_ip = self.ip
                    
                    # Push argument for the function
                    self.stack.append(arg_val)
                    
                    # Jump to function body
                    self.ip = self._find_label(func_label)
                    
                    # Save current state to call stack
                    self.call_stack.append((return_ip, self.variables.copy()))
                    
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

# Add additional bytecode-related methods to compiler
def _compile_array(self, node):
    """Compile array creation"""
    for element in node.elements:
        self._compile_node(element)
    self.emit("CREATE_ARRAY", len(node.elements))

def _compile_array_access(self, node):
    """Compile array access expression"""
    self._compile_node(node.array)
    self._compile_node(node.index)
    self.emit("LOAD_ARRAY_ITEM")

def _compile_array_assign(self, node):
    """Compile array element assignment"""
    self._compile_node(node.array)
    self._compile_node(node.index)
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
    # (label, param_name, return_type)
    func_meta = (func_label, node.a, node.rt)
    func_meta_idx = self.add_constant(func_meta)
    
    # Create a function object and store it in the variable
    self.emit("LOAD_CONST", func_meta_idx)
    self.emit("MAKE_FUNCTION")
    self.emit("STORE_VAR", self.variables[node.n])
    
    # Jump over the function code
    self.emit("JUMP", end_label)
    
    # Function body starts here
    self.emit("LABEL", func_label)
    
    # Add parameter to variables
    if node.a not in self.variables:
        self.variables[node.a] = len(self.variables)
    
    # Store the parameter value passed on the stack
    self.emit("STORE_VAR", self.variables[node.a])
    
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
    
    # Evaluate and push argument
    self._compile_node(node.a)
    
    # Call the function
    self.emit("CALL_FUNCTION", 1)  # 1 argument

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
        case ArrayAccess(array, index):
            self._compile_array_access(node)
        case ArrayAssign(array, index, value):
            self._compile_array_assign(node)
        case Length(expr):
            self._compile_length(node)
        case Slice(sequence, start, end):
            self._compile_slice(node)
        case Fun(n, a, at, rt, b, e):
            self._compile_function(node)
        case Call(n, a):
            self._compile_call(node)
        case Return(expr):
            self._compile_return(node)
        case Dict(pairs):
            self._compile_dict(node)
        case DictAccess(dict, key):
            self._compile_dict_access(node)
        case DictAssign(dict, key, value):
            self._compile_dict_assign(node)
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

# def test_slice_array():
code = """
            int x = 1;
            int z = 100;
            fun foo(y : int) : int{
                x = 2;
                println(z);
                return x;
            }
            println(foo(10));
            println(z);
            println(x);
        """

# code2 = """
# fun add(a: int, b: int): int {
#     return a + b;
# }
# dict d = {"sum": add(3, 4)};
# int result = d{"sum"};
# println(result);
# """

code3="""
            int[] arr = [10, 20, 30];
            int[] slice = arr[0:2];
            slice[0]=100;
            println(slice[0]);
            println(arr[0]);
            """
ast = parse(code3)
print(e(ast))


# def run_test_case(code, expected_output):
#     from io import StringIO
#     import sys
#     print("yes")
#     # Redirect stdout to capture print statements
#     old_stdout = sys.stdout
#     sys.stdout = StringIO()
    
#     try:
#         print("2")
#         ast = parse(code)
#        
#         e(ast)
#         actual_output = sys.stdout.getvalue().strip()
#         print(f"Expected: {expected_output}, Got: {actual_output}")
#         assert actual_output == expected_output, f"Expected: {expected_output}, Got: {actual_output}"
#         return "Test passed"
#     except Exception as ex:
#         return f"Test failed: {ex}"
#     finally:
#         sys.stdout = old_stdout

# test_slice_array()
# Modify the main entry point to support interpretation or compilation
# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) > 1:
#         filename = sys.argv[1]
#         mode = sys.argv[2] if len(sys.argv) > 2 else "interpret"
        
#         with open(filename, 'r') as f:
#             code = f.read()
        
#         ast = parse(code)
#         if mode == "compile":
#             # Compile and run with bytecode VM
#             compile_and_run(ast)
#         else:
#             # Use the interpreter
#             e(ast)
#     else:
#         from tests.unit_tests import run_tests
#         run_tests()