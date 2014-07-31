
from vmdata import *

# exception to raise when vm should terminate
class StopExecution(Exception):
	pass

# Instructions:
class AbstractOp:
	# default value
	arity = 0
	def __init__(self, *args):
		assert len(args) == self.arity
		self.args = args
		# store args also as string for easier output
		self.str_args = map(str, args)

	# dump as a instruction on lambda man language
	def to_source(self):
		return ' '.join([self.name] + self.str_args)

	def __repr__(self):
		return '{}({})'.format(self.__class__, ', '.join(self.str_args))


# push to data stack integer N
class LoadConstant(AbstractOp):
	name = 'LDC'
	arity = 1

	def mutate(self, vm):
		vm.data_stack.append(VmInteger(self.args[0]))
		vm.counter += 1

# push to data stack
# from n-th frame i-th value
#
# frame[n][i] --> stack
class LoadEnv(AbstractOp):
	name = 'LD'
	arity = 2

	def mutate(self, vm):
		n, i = self.args

		# go n frames up
		frame = go_to_nth_parent(vm.current_frame, n)
		assert frame.tag != Tag.DUMMY_FRAME

		# push the i-th elemt
		value = frame.values[i]
		vm.data_stack.append(value)
		vm.counter += 1
FrameToStack = LoadEnv

# save top value from data stack
# to n-th frame as i-th value
#
# stack --> frame[n][i]
class StoreToEnv(AbstractOp):
	name = 'ST'
	arity = 2

	def mutate(self, vm):
		# go n frames up
		n, i = self.args
		frame = go_to_nth_parent(vm.current_frame, n)
		assert frame.tag != Tag.DUMMY_FRAME

		value = vm.data_stack.pop()
		frame.values[i] = value
		vm.counter += 1

# synonim:
SaveToEnv = StoreToEnv


class IntOperation(AbstractOp):
	def mutate(self, vm):
		# self.func should be reloaded
		self.mutate_arithmetic(vm, self.func)

	@staticmethod
	def mutate_arithmetic(vm, func):
		v2 = vm.data_stack.pop()
		v1 = vm.data_stack.pop()
		assert (v1.tag == Tag.INTEGER)
		assert (v2.tag == Tag.INTEGER)
		c = func(v1.n, v2.n)
		vm.data_stack.append(VmInteger(c))
		vm.counter += 1

class IntAddition(IntOperation):
	name = 'ADD'
	@staticmethod
	def func(x, y):
		return x + y


class IntSubtraction(IntOperation):
	name = 'SUB'
	@staticmethod
	def func(x, y):
		return x - y


class IntMultiplication(IntOperation):
	name = 'MUL'
	@staticmethod
	def func(x, y):
		return x * y

class IntDivision(IntOperation):
	name = 'DIV'
	@staticmethod
	def func(x, y):
		return x / y

class CompareEqual(IntOperation):
	name = 'CEQ'
	@staticmethod
	def func(x, y):
		if x == y:
			return 1
		else:
			return 0

class CompareGreater(IntOperation):
	name = 'CGT'
	@staticmethod
	def func(x, y):
		if x > y:
			return 1
		else:
			return 0

class CompareGreaterOrEqual(IntOperation):
	name = 'CGTE'
	@staticmethod
	def func(x, y):
		if x >= y:
			return 1
		else:
			return 0

class IsInteger(AbstractOp):
	name = 'ATOM'
	def mutate(self, vm):
		x = vm.data_stack.pop()
		if x.tag == Tag.INTEGER:
			y = 1
		else:
			y = 0
		vm.data_stack.append(VmInteger(y))
		vm.counter += 1

class AllocateCons(AbstractOp):
	name = 'CONS'
	def mutate(self, vm):
		y = vm.data_stack.pop()
		x = vm.data_stack.pop()
		z = VmCons(x, y)
		vm.data_stack.append(z)
		vm.counter += 1

class ExtractFirst(AbstractOp):
	name = 'CAR'
	def mutate(self, vm):
		x = vm.data_stack.pop()
		assert (x.tag == Tag.CONS)

		y = x.first
		vm.data_stack.append(y)
		vm.counter += 1

class ExtractSecond(AbstractOp):
	name = 'CDR'
	def mutate(self, vm):
		x = vm.data_stack.pop()
		assert (x.tag == Tag.CONS)

		y = x.second
		vm.data_stack.append(y)
		vm.counter += 1

# jump to instruction based on
# top value form data_stack
class ConditionalBranch(AbstractOp):
	name = 'SEL'
	arity = 2

	def mutate(self, vm):
		go_true, go_false = self.args
		assert (x.tag == Tag.INTEGER)

		vm.control_stack.append(JoinAddress(vm.counter + 1))
		if x == 0:
			vm.counter = go_false
		else:
			vm.counter = go_true

class ReturnFromBranch(AbstractOp):
	name = 'JOIN'
	def mutate(self, vm):
		x = vm.control_stack.pop()
		assert (x.tag == Tag.JOIN)
		vm.counter = x.value

class TailCallBranch(AbstractOp):
	name = 'TSEL'
	arity = 2

	def mutate(self, vm):
		go_true, go_false = self.args

		x = vm.data_stack.pop()
		assert (x.tag == Tag.INTEGER)
		if x.n == 0:
			vm.counter = go_false
		else:
			vm.counter = go_true

class LoadFunction(AbstractOp):
	name = 'LDF'
	arity = 1

	def mutate(self, vm):
		# address from which to load function
		(address, ) = self.args

		closure = VmClosure(address, vm.current_frame)
		vm.data_stack.append(closure)
		vm.counter += 1

class CallFunction(AbstractOp):
	name = 'AP'
	arity = 1

	def mutate(self, vm):
		# n -- number of arguments
		(n, ) = self.args

		closure = vm.data_stack.pop()
		assert closure.tag == Tag.CLOSURE

		address = closure.address
		frame = closure.frame

		# create new frame for the call
		new_frame = EnvFrame(n)
		new_frame.parent = frame

		# copy n values from stack into frame
		new_frame.copy_from_stack(vm, n)

		# save frame pointer
		vm.control_stack.append(vm.current_frame)
		# save return address
		vm.control_stack.append(ReturnAddress(vm.counter + 1))

		# establish new env
		vm.current_frame = new_frame
		# and jump to address
		vm.counter = address


class ReturnFromFunction(AbstractOp):
	name = 'RTN'

	def mutate(self, vm):
		# pop return address
		address = vm.control_stack.pop()
		if address.tag == Tag.STOP:
			raise StopExecution()
		assert (address.tag == Tag.RETURN)
		# pop frame pointer
		frame = vm.control_stack.pop()

		# restore env
		vm.current_frame = frame
		# jump to return address
		vm.counter = address.value

# create dummy frame of size n
# and go to it
class EmptyEnv(AbstractOp):
	name ='DUM'
	arity = 1
	def mutate(self, vm):
		# n -- size of a frame to allocate
		(n, ) = self.args

		frame = EnvFrame(n)
		frame.parent = vm.current_frame
		frame.tag = Tag.DUMMY_FRAME
		vm.current_frame = frame

		vm.counter += 1

class RecursiveCallFunction(AbstractOp):
	name = 'RAP'
	arity = 1

	def mutate(self, vm):
		# n -- number of arguments to copy
		(n, ) = self.args

		closure = vm.data_stack.pop()
		assert closure.tag == Tag.CLOSURE

		address = closure.address
		frame = closure.frame

		assert vm.current_frame.tag == Tag.DUMMY_FRAME
		assert frame.get_size() == n
		frame.copy_from_stack(vm, n)

		next_frame = vm.current_frame.parent

		# save frame pointer and return address
		vm.control_stack.append(next_frame)
		vm.control_stack.append(ReturnAddress(vm.counter + 1))

		vm.current_frame = frame
		# make the frame normal
		vm.current_frame.tag = Tag.GOOD_FRAME
		vm.counter = address

# is not supported by ABI
class Stop(AbstractOp):
	name = 'STOP'

class TailCallFunction(AbstractOp):
	name = 'TAP'
	arity = 1

	def mutate(self, vm):
		# n -- number of arguments to copy
		(n, ) = self.args
		closure = vm.data_stack.pop()
		assert (closure.tag == Tag.CLOSURE)

		address = closure.address
		frame = closure.frame
		new_frame = EnvFrame(n)
		new_frame.parent = vm.current_frame

		frame.copy_from_stack(vm, n)

		vm.current_frame = new_frame
		vm.counter = address

class RecursiveTailCallFunction(AbstractOp):
	name = 'TRAP'
	arity = 1

	def mutate(self, vm):
		# n -- number of arguments to copy
		(n, ) = self.args
		closure = vm.data_stack.pop()
		assert (closure.tag == Tag.CLOSURE)

		address = closure.address
		frame = closure.frame

		assert vm.current_frame.tag == Tag.DUMMY_FRAME
		assert vm.current_frame.get_size() == n
		frame.copy_from_stack(vm, n)

		vm.current_frame = frame
		vm.counter = address

class DebugPrint(AbstractOp):
	name = 'DBUG'
	def mutate(self, vm):
		value = vm.data_stack.pop()
		print 'Value on top of stack was', value
		vm.trace_output.append(repr(value))
		vm.counter += 1


ALL_INSTRUCTIONS = [
	LoadConstant,
	LoadEnv,
	IntAddition,
	IntSubtraction,
	IntMultiplication,
	IntDivision,
	CompareEqual,
	CompareGreater,
	CompareGreaterOrEqual,
	IsInteger,
	AllocateCons,
	ExtractFirst,
	ExtractSecond,
	ConditionalBranch,
	ReturnFromBranch,
	LoadFunction,
	CallFunction,
	ReturnFromFunction,
	EmptyEnv,
	RecursiveCallFunction,
	Stop,
	TailCallBranch,
	TailCallFunction,
	RecursiveTailCallFunction,
	StoreToEnv,
	DebugPrint,
]
