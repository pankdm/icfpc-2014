
import os
import sys
# magic spell to include files from outer dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lisp import Lisp
import sys


cons1 = """
LDC  11
LDC  12
LDC  13
LDC  14
LDC  0
CONS
CONS
CONS
CONS
LDC  21
LDC  22
LDC  23
LDC  24
LDC  0
CONS
CONS
CONS
CONS
LDC  0
CONS
CONS
CAR
RTN
"""

def main():
	lisp = Lisp()
	lisp.load_program(cons1)
	if len(sys.argv) > 1:
		lisp.trace()
	else:
		lisp.run()

if __name__ == '__main__':
	main()

