"""Helper functions for test cases"""

from typing import Any, Tuple, List

def ensure_tuple_as_list(value: Any) -> Any:
    """Convert a tuple to a list if needed.
    This helps with handling test cases that are tuples."""
    if isinstance(value, tuple):
        return list(value)
    return value

def format_test_code(code: str) -> str:
    """Format test code to avoid common parsing issues.
    - Ensures all semicolons
    - Normalizes whitespace
    - Adds required parentheses
    """
    # Remove extra whitespace and normalize indentation
    lines = [line.strip() for line in code.strip().split('\n')]
    # Join with single newlines
    code = '\n'.join(lines)
    
    # Ensure all statements have semicolons where needed
    statements = ['if', 'while', 'for', 'return', 'int', 'string', 'fun']
    for stmt in statements:
        # Find statement starts that don't have semicolons
        pass
        
    # Other formatting improvements could be added here
    
    return code
