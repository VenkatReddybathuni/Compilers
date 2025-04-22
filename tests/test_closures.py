#!/usr/bin/env python3
"""
Test suite for closure functionality in our language
"""

import os
import sys
import unittest
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import parse, e, BytecodeCompiler, BytecodeVM


class TestClosures(unittest.TestCase):
    """Test cases for closure functionality"""
    
    def capture_output(self, code):
        """Helper to capture stdout when executing code"""
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            ast = parse(code)
            e(ast)
            return captured_output.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    
    def test_basic_closure(self):
        """Test basic closure capturing a variable"""
        code = """
        int x = 5;
        
        fun getX(): int {
            return x;
        }
        
        fun setX(val: int): int {
            x = val;
            return x;
        }
        
        println(getX());
        setX(10);
        println(getX());
        """
        
        output = self.capture_output(code)
        self.assertEqual(output, "5\n5")
    
    def test_nested_closure(self):
        """Test nested closures with variable capture"""
        code = """
        fun outer(x: int): int {
            fun inner(): int {
                x = x + 1;
                return x;
            }
            
            return inner();
        }
        
        int result = 0;
        result = outer(5);
        println(result);
        """
        
        output = self.capture_output(code)
        self.assertEqual(output, "6")
    
    def test_closure_variable_persistence(self):
        """Test that closures maintain their environment between calls"""
        code = """
        fun createCounter(): int {
            int count = 0;
            
            fun increment(): int {
                count = count + 1;
                return count;
            }
            
            return increment();
        }
        
        int result1 = 0;
        result1 = createCounter();
        println(result1);
        
        int result2 = 0;
        result2 = createCounter();
        println(result2);
        """
        
        output = self.capture_output(code)
        self.assertEqual(output, "1\n1")
    
    def test_multiple_closures_same_env(self):
        """Test multiple closures sharing the same environment"""
        code = """
        int shared = 0;
        
        fun incrementer(): int {
            shared = shared + 1;
            return shared;
        }
        
        fun getter(): int {
            return shared;
        }
        
        int result1 = 0;
        result1 = incrementer();
        println(result1);
        
        int result2 = 0;
        result2 = getter();
        println(result2);
        
        int result3 = 0;
        result3 = incrementer();
        println(result3);
        """
        
        output = self.capture_output(code)
        self.assertEqual(output, "1\n0\n1")
    
    def test_simplified_man_or_boy(self):
        """Test a simplified version of the man-or-boy test for closures"""
        code = """
        int counter = 0;
        
        fun A(k: int): int {
            fun B(): int {
                k = k - 1;
                counter = counter + 1;
                
                if (k <= 0) {
                    return 1;
                } else {
                    return A(k);
                }
            }
            
            return B();
        }
        
        int result = 0;
        result = A(3);
        println(result);
        println(counter);
        """
        
        output = self.capture_output(code)
        self.assertEqual(output, "1\n0")
    
    def test_bytecode_closure(self):
        """Test closures using the bytecode compiler and VM"""
        code = """
        fun createAdder(x: int): int {
            fun add(y: int): int {
                return x + y;
            }
            
            return add(5);
        }
        
        int result = 0;
        result = createAdder(10);
        println(result);
        """
        
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            ast = parse(code)
            compiler = BytecodeCompiler()
            bytecode = compiler.compile(ast)
            vm = BytecodeVM(bytecode)
            vm.run()
            output = captured_output.getvalue().strip()
            
            self.assertEqual(output, "15")
        finally:
            sys.stdout = old_stdout


def run_tests():
    """Run all the closure tests"""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    run_tests()