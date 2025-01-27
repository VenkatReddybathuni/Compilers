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

@dataclass
class Sequence(AST):
    statements: list[AST]

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

def e(tree: AST, env=None) -> int | bool | str:
    if env is None:
        env = {}

    match tree:
        case Number(v):
            return int(v)
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
            return str(e(l, env)) + str(e(r, env))
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
        case Var(name):
            return env[name]
        case Assign(name, expr):
            env[name] = e(expr, env)
            return env[name]
        case Let(var, expr, body):
            # Create a new scope
            new_env = env.copy()
            new_env[var] = e(expr, env)
            return e(body, new_env)


def lex(s: str) -> Iterator[Token]:
    i = 0
    while i < len(s):  # Changed from while True
        while i < len(s) and s[i].isspace():
            i += 1

        if i >= len(s):
            return

        if s[i].isalpha():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isalpha():
                t = t + s[i]
                i = i + 1
            if t in {"and", "or", "let", "be", "in", "end", "if", "then", "else", "while", "do"}: 
                yield KeywordToken(t)
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
                case '+' | '*' | '<' | '=' | '-' | '/' | '%' | '>' | '!' | '(' | ')' | ';':  # Added semicolon
                    i += 1
                    if i < len(s):
                        next_char = s[i]
                        if (t + next_char) in {'**', '++', '<=', '>=', '==', '!='}:  # Check for two-char operators
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
            stmt = parse_stmt()
            statements.append(stmt)
            
            # Skip semicolons
            while t.peek(None) is not None and isinstance(t.peek(), OperatorToken) and t.peek().o == ';':
                next(t)
                
            # Break if we hit end of statement or certain keywords
            if t.peek(None) is None or (isinstance(t.peek(), KeywordToken) and t.peek().w in {'end', 'else'}):
                break
                
        return Sequence(statements) if len(statements) > 1 else statements[0]

    def parse_stmt():
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_expr()
                expect(KeywordToken("then"))
                then = parse_stmt() 
                expect(KeywordToken("else"))
                else_ = parse_stmt()  
                expect(KeywordToken("end"))
                return If(cond, then, else_)
            case _:
                return parse_expr()

    def parse_expr():
        return parse_assign()  

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
            case VarToken(v):
                next(t)
                return Var(v)
            case StringToken(v):
                next(t)
                return String(v)
            case KeywordToken("let"):
                next(t)
                if not isinstance(t.peek(None), VarToken):
                    raise ParseError("Expected variable name after 'let'")
                var = next(t).v
                expect(KeywordToken("be"))
                expr = parse_expr()
                expect(KeywordToken("in"))
                body = parse_stmt()  
                expect(KeywordToken("end"))
                return Let(var, expr, body)
            case _:
                raise ParseError(f"Unexpected token: {t.peek(None)}")

    return parse_stmt()  


# Example usage:
test_cases = [
    'if x >= 10 and y <= 20 then x + y else x - y end',
    '2 ** 3',  # Power operation
    '17 % 5',  # Modulo operation
    '"Hello" ++ " World"',  # String concatenation
    'x == y',  # Equality comparison
    'x != y',  # Inequality comparison
    '(2 + 3) * 4',  # Should evaluate to 20
    '2 + (3 * 4)',  # Should evaluate to 14
    'if (x > 10) then (x + y) else (x - y) end',
    '(2 ** 3) + 1',  # Should evaluate to 9
    '((2 + 3) * (4 + 5))',  # Should evaluate to 45
]

# Run test cases
test_env = {"x": 15, "y": 10}  # Set up environment with test variables
print("\nRunning test cases:")
for test in test_cases:
    try:
        result = e(parse(test), test_env)
        print(f"Test: {test}")
        print(f"Result: {result}")
        print("-" * 30)
    except Exception as err:
        print(f"Error in test '{test}': {err}")
        print("-" * 30)

# Test specifically for the if condition
print("\nTesting if condition:")
test_env = {"x": 15, "y": 10}
test = 'if ((x == 15) and y < 20) then (x + y)*y else (x - y) end'
result = e(parse(test), test_env)
print(f"Test: {test}")
print(f"Result: {result}")  # Should print 25 (15 + 10)

# Add a test case to verify the fix
print("\nTesting comparison operators:")
test_env = {"x": 15, "y": 10}
comparison_tests = [
    'x > 10',  # Should be True
    'if x > 10 then x + y else x - y end',  # Should be 25
    'x >= 15',  # Should be True
    'y < x',  # Should be True
]

for test in comparison_tests:
    try:
        result = e(parse(test), test_env)
        print(f"Test: {test}")
        print(f"Result: {result}")
        print("-" * 30)
    except Exception as err:
        print(f"Error in test '{test}': {err}")
        print("-" * 30)

# Update test cases
let_tests = [
    "let a be 3 in a + a end",  # Should be 6
    "let a be 3 in let b be a + 2 in a + b end end",  # Should be 8
    "let x be 5 in let y be x * 2 in x + y end end",  # Should be 15
    "let x be (2*5) in let y be (x + 3) in x + y end end",  # Should be 23
    "let a be 3 in if a == 3 then 1+1 else 2+2 end end",  # Should now work
    "let x be 10 in if x > 5 then x + 2 else x - 2 end end"  # Additional test
]


print("\nTesting let expressions:")
for test in let_tests:
    try:
        result = e(parse(test))
        print(f"Test: {test}")
        print(f"Result: {result}")
        print("-" * 30)
    except Exception as err:
        print(f"Error in test '{test}': {err}")
        print("-" * 30)
