# first need to install:
# "pip install enum34"
from enum import Enum


# VM Tags
class Tag(Enum):
	INTEGER = 0
	CONS = 1
	CLOSURE = 2
	DUMMY_FRAME = 3
	GOOD_FRAME = 4
	STOP = 5
	RETURN = 6
	JOIN = 7

class VmData(object):
	def __init__(self, tag):
		self.tag = tag
	def __repr__(self):
		return 'VmData({})'.format(repr(self.tag))


# control commands:


def go_to_nth_parent(frame, n):
	while n > 0:
		frame = frame.parent
		n -= 1
	return frame

class EnvFrame(VmData):
	def __init__(self, size):
		self.parent = None
		self.values = [None] * size
		VmData.__init__(self, Tag.GOOD_FRAME)
	def __repr__(self):
		if self.tag == Tag.DUMMY_FRAME:
			return 'TAG_DUM (size {})'.format(len(self.values))
		return 'EnvFrame({})'.format(repr(self.values))

	# n -- number of valeus
	def copy_from_stack(self, vm, n):
		i = n - 1
		while i >= 0:
			y = vm.data_stack.pop()
			self.values[i] = y
			i -= 1

	def get_size(self):
		return len(self.values)

	def dump(self):
		print self
		if self.parent != None:
			self.parent.dump()

class ReturnAddress(VmData):
	def __init__(self, value):
		self.value  = value
		VmData.__init__(self, Tag.RETURN)
	def __repr__(self):
		return 'ReturnAddress({})'.format(self.value)

class JoinAddress(VmData):
	def __init__(self, value):
		self.value = value
		VmData.__init__(self, Tag.JOIN)
	def __repr__(self):
		return 'JoinAddress({})'.format(self.value)

class VmInteger(VmData):
	def __init__(self, n):
		self.n = n
		VmData.__init__(self, Tag.INTEGER)
	# def __repr__(self):
	# 	return 'VmInteger({})'.format(self.n)
	def __repr__(self):
		return '{}'.format(self.n)

class VmCons(VmData):
	def __init__(self, first, second):
		self.first = first
		self.second = second
		VmData.__init__(self, Tag.CONS)

	def __repr__(self):
		return '({}, {})'.format(self.first, self.second)

class VmClosure(VmData):
	def __init__(self, address, frame):
		self.address = address
		self.frame = frame
		VmData.__init__(self, Tag.CLOSURE)
	def __repr__(self):
		return '{{ {} <env> }}'.format(self.address)
		# return 'VmClosure({},{})'.format(self.address, self.frame)
