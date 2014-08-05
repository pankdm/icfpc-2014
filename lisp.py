
# first need to install:
# "pip install enum34"
from enum import Enum
import sys

from vmdata import *
from instructions import *

# Lisp virtual machine that contains all data structures
class VM:
	def __init__(self):
		self.counter = 0
		self.data_stack = []
		self.current_frame = EnvFrame(2)
		self.control_stack = [VmData(Tag.STOP)]
		self.trace_output = []

	def dump(self):
		print 'counter = ', self.counter
		print 'data_stack (%s) = '
		for data in reversed(self.data_stack):
			print data
		print
		print 'current_frame (%e) = '
		if self.current_frame != None:
			self.current_frame.dump()
		print
		print 'control_stack (%d) = '
		for control in self.control_stack:
			print control

def strip_comments(s):
	return s.split(';')[0].strip()

def parse_line(s):
	without_comment = strip_comments(s)
	ops = without_comment.split()
	if len(ops) == 0:
		print 'Skipping empty lines'
		return None

	op = ops[0]
	for op_class in ALL_INSTRUCTIONS:
		if op_class.name == op:
			print 'returning', op
			# convert all arguments to in
			int_args = map(int, ops[1:])
			return op_class(*int_args)
	print 'Unknown instruction:', op


class Lisp:
	def __init__(self):
		self.vm = VM()
		self.program = []
		self.program_code = []
		self.step = 0
		self.debug_output = True

	def load_program_from_file(self, file_name):
		f = open(file_name, 'rt')
		content = f.read()
		print content
		self.load_program(content)

	def load_program(self, content):
		for s in content.split('\n'):
			instruction = parse_line(s)
			if instruction != None:
				self.program.append(instruction)
				self.program_code.append(strip_comments(s))

	def trace(self):
		try:
			while (True):
				self.next_step()
				raw_input()
		except StopExecution:
			print 'Execution was stopped'
			self.dump()
			pass

	def run(self):
		self.debug_output = False
		try:
			while (True):
				self.next_step()
		except StopExecution:
			print 'Execution was stopped'
			self.dump()
			pass

	def next_step(self):
		index = self.vm.counter
		op = self.program[index]
		if self.debug_output:
			self.dump()
			print
		line = self.program_code[index]
		if self.debug_output:
			print 'address =', self.vm.counter
		print 'Executing mutate on {} ("{}")'.format(repr(op), line)
		op.mutate(self.vm)
		self.step += 1

	def dump(self):
		print
		print
		print 'step = ', self.step
		self.vm.dump()



def main():
	lisp = Lisp()

	if len(sys.argv) > 1:
		program_file = sys.argv[1]
	else:
		program_file = 'lambda-ai/local.gcc'

	lisp.load_program_from_file(program_file)
	# lisp.load_program_from_file('lambda-ai/goto.gcc')

	if len(sys.argv) > 2:
		lisp.trace()
	else:
		lisp.run()

if __name__ == '__main__':
    main()


