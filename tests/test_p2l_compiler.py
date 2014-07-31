# magic spells to include files from outer dir
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from p2l_compiler import P2LCompiler, read_code

from unittest import TestCase

# dummy test case, just to use nice assertions from python unittest lib
t = TestCase("__str__")

def test_simple():
    p2l = P2LCompiler()
    byteCode = p2l.compile_expr('PRINT(10 + 15)')

    output = \
"""LDC 10
LDC 15
ADD
DBUG
"""
    t.assertEquals(byteCode.to_source(), output)


def test_any():
    if len(sys.argv) > 1:
        code = read_code(sys.argv[1])
    else:
        code = read_code('p2l/1.lisp.py')
    # parseprint(code)

    p2l = P2LCompiler()
    byteCode = p2l.compile_expr(code)
    print
    byteCode.show()


def main():
    test_simple()
    test_any()

if __name__ == '__main__':
    main()
