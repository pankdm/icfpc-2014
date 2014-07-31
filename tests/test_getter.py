
import os
import sys
# magic spell to include files from outer dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lisp import Lisp

getter = """
LDF  15   ; load main. This program creates simple map: [[11,12,13,14], [21,22,23,24]] an then access some element of this array [] - have 0 in the end.
AP   0
RTN
LD 0 0 ;:GETTER PUT
LD 0 1
TSEL 6 13;FOR LOOP INITIAL CONDITION
CDR
LD 0 1
LDC 1
SUB
ST 0 1
LD 0 1
TSEL 6 13
CAR
RTN
LDC  11;:MAIN
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
LDC 1
LDF 3;GETTER
AP 2
LDC 2
LDF 3;GETTER
AP 2
RTN
"""

def main():
	lisp = Lisp()
	lisp.load_program(getter)
	if len(sys.argv) > 1:
		lisp.trace()
	else:
		lisp.run()

	# check last element
	result = lisp.vm.data_stack[-1]
	assert result.n == 23


if __name__ == '__main__':
	main()
