# magic spells to include files from outer dir
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from astpp import *
import ast

def read_code(file_name):
	f = open(file_name, 'rt')
	code = ''.join(f.readlines())
	return code


class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

code = read_code('emulator.py')
tree = ast.parse(code)
FuncLister().visit(tree)


