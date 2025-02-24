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
    
    for u, uv in reversed(env):
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

            call_env = env.copy()
            call_env.append((param, arg_value))
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
                
            # Check if this is an array type (e.g. "int[]")
            is_array = False
            if i + 1 < len(s) and s[i] == '[' and s[i + 1] == ']':
                is_array = True
                i += 2
                
            if t in {"and", "or", "if", "else", "fun", "return", "println", "str", "while", "continue", "break"}:  # Added while, continue, break
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
    t = peekable(lex(s))

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
        match t.peek(None):
            case TypeToken(typ, is_array):
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError(f"Expected variable name after {typ}")
                var = next(t).v
                var_type = f"{typ}[]" if is_array else typ
                expect(OperatorToken("="))
                
                if is_array:
                    if not isinstance(t.peek(None), OperatorToken) or t.peek().o != '[':
                        raise ParseError(f"Expected array literal after {var}")
                    array_expr = parse_atom()
                    let_node = Let(var, array_expr, None, var_type)
                    array_expr.parent = let_node
                    expect(OperatorToken(";"))
                    next_stmt = parse_statements() if t.peek(None) is not None else None
                    let_node.body = next_stmt if next_stmt else Sequence([])
                    return let_node
                
                # Check for function call
                if isinstance(t.peek(None), VarToken):
                    func_name = next(t).v
                    if t.peek(None) == OperatorToken("("):
                        next(t)
                        arg = parse_expr()
                        expect(OperatorToken(")"))
                        expect(OperatorToken(";"))
                        return Let(var, Call(func_name, arg), Sequence([]))
                    t.prepend(VarToken(func_name))  # Put back the token if not a function call
                
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
                    if not isinstance(t.peek(None), OperatorToken) or t.peek().o != ']':
                        raise ParseError("Expected closing bracket ']'")
                    next(t)  # consume ]
                    
                    if isinstance(t.peek(None), OperatorToken) and t.peek().o == '=':
                        next(t)  # consume =
                        value = parse_expr()
                        return ArrayAssign(Var(name), index, value)
                    return ArrayAccess(Var(name), index)
                    
                # ...rest of VarToken handling...
                if t.peek(None) == OperatorToken("="):
                    # ... existing assignment handling ...
                    if t.peek(None) == OperatorToken("="):
                        next(t)
                        # Check for function call
                        if isinstance(t.peek(None), VarToken):
                            func_name = next(t).v
                            if t.peek(None) == OperatorToken("("):
                                next(t)
                                arg = parse_expr()
                                expect(OperatorToken(")"))
                                expect(OperatorToken(";"))
                                return Let(name, Call(func_name, arg), Sequence([]))
                            t.prepend(VarToken(func_name))  # Put back the token if not a function call
                        # Handle normal expression assignment
                        expr = parse_expr()
                        expect(OperatorToken(";"))
                        return Let(name, expr, Sequence([]))
                elif t.peek(None) == OperatorToken("("):
                    next(t)
                    arg = parse_expr()
                    expect(OperatorToken(")"))
                    # Don't consume semicolon here, let the statement level handle it
                    return Call(name, arg)
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
