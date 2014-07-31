from collections import namedtuple

from instructions import *
from p2l_labels import *
from p2l_config import P2LConfig

def assert_type(obj, class_type):
    if isinstance(obj, class_type):
        return
    assert False, 'Type mismatch, expected {}, got {}'.format(
        class_type,
        str(obj))

def assert_not_type(obj, class_type):
    if not isinstance(obj, class_type):
        return
    print obj
    assert False

# data to store function definition in compiler
class FunctionImpl:
    def __init__(self, name, byte_code):
        self.name = name
        # required paramter
        self.arity = None
        self.dummy_arity = 0
        self.byte_code = byte_code

# class
ArrayAllocation = namedtuple(
    'ArrayAllocation',
    ['offset', 'size'],
    verbose = True
)

# class to represent
# all names in current scope
# (this includes usual variables and arrays)
class ScopeVariables:
    def __init__(self):
        self.vars = {}
        self.arrays = {}

        # last free index for allocation
        self.free_index = P2LConfig.NUM_REGISTERS

        # counter for number of local variables allocated
        self.dummy_slots = 0

    def declare_variable(self, var_name, is_local):
        # TODO: check conflicts
        self.vars[var_name] = self.free_index
        self.free_index += 1

        if is_local:
            self.dummy_slots += 1

    def declare_array(self, array_name, size):
        allocation = ArrayAllocation(
            offset=self.free_index,
            size=size
        )
        self.arrays[array_name] = allocation
        self.free_index += size
        self.dummy_slots += size

    def array_offset(self, array_name):
        allocation = self.arrays[array_name]
        return allocation.offset

    def is_declared(self, var_name):
        return var_name in self.vars

    def total_slots_allocated(self):
        return self.free_index

    def dummy_slots_allocated(self):
        return self.dummy_slots

    def produce_get_for_array(self, array_name, index):
        allocation = self.arrays[array_name]
        absolute_index = allocation.offset + index

        byte_code = ByteCode()
        byte_code.append( LoadEnv(0, absolute_index) )

    def produce_get_byte_code(self, var_name):
        # returns byte code needed to
        # 1) take value of @var_name
        # 2) push onto data stack

        if var_name not in self.vars:
            # @var_name is likely global
            return None

        index = self.vars[var_name]
        byte_code = ByteCode()
        byte_code.append( LoadEnv(0, index) )
        return byte_code

    def produce_assign_byte_code(self, var_name):
        # returns byte code needed to
        # 1) pop value from data stack
        # 2) save this value in @var_name

        index = self.vars[var_name]
        # save the value to current frame

        byte_code = ByteCode()
        byte_code.append( StoreToEnv(0, index) )
        return byte_code


class CompilationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

# byte code represents a sequence of instructions
# for vm to executre
class ByteCode:
    def __init__(self):
        self.output = []

    @staticmethod
    def from_list(output):
        byte_code = ByteCode()
        byte_code.output = output
        return byte_code

    def append(self, op):
        assert_not_type(op, ByteCode)
        self.output.append(op)

    def append_byte_code(self, byte_code):
        assert_type(byte_code, ByteCode)
        self.output += byte_code.output


    def show(self):
        print 'ByteCode output of size {}:'.format(len(self.output))
        for op in self.output:
            print op, ' |||| ',  op.to_source()

    def show_without_source(self):
        print 'ByteCode output of size {}:'.format(len(self.output))
        for index, op in enumerate(self.output):
            print '{}: \t {}'.format(index, op)

    def dump_without_source(self):
        result = ['ByteCode output of size {}:'.format(len(self.output))]
        for index, op in enumerate(self.output):
            # {:d} -- means aligning integers
            result.append( '{:d}:     {}'.format(index, op) )
        return '\n'.join(result)


    def to_source(self):
        result = ''
        for op in self.output:
            result += op.to_source()
            result += '\n'
        return result

class EmptyByteCode(ByteCode):
    pass




# instructions of this type will be replaced with the byte code,
# returned by function @expand
class IExpandable:
    def expand(self):
        assert False

    def to_source(self):
        raise CompilationError(
            '{} wasnt expanded'.format(self.__class__)
        )

# internal compiler instructions
# that are used during code generation
class ApplyFunction(IExpandable):
    def __init__(self, name, arity, dummy_arity):
        self.name = name
        self.arity = arity
        self.dummy_arity = dummy_arity

    def __repr__(self):
        return 'ApplyFunction "{}" (arity = {}, dummy = {})'.format(
                self.name,
                self.arity,
                self.dummy_arity
            )

    def expand(self):
        output = []
        # add dummy variables to stack
        for i in xrange(self.dummy_arity):
            output.append( LoadConstant(0) )

        # count size of frame to be allocated
        num_variables = P2LConfig.NUM_REGISTERS
        num_variables += self.arity
        num_variables += self.dummy_arity

        output += [
            LoadFunctionLabel(self.name),
            CallFunction(num_variables)
        ]
        result = ByteCode.from_list(output)
        print result
        return result


# executing of expansion of this byte code have following effect:
# stack --> get(x)
# Load(n, x)
class LoadEnvGeneric(IExpandable):
    def __init__(self, n):
        if n != 0:
            raise CompilationError(
                'LoadEnvGeneric is only supported from 0 frame')
        self.n = n

    def __repr__(self):
        return 'LoadToEnvGeneric({})'.format(
                self.n,
            )


    def expand(self):
        x_register = LapshaLoadImplementation.X_REGISTER
        output = [
            StoreToEnv(self.n, x_register),
            UnconditionalJumpLabelSEL(LAPSHA_LOAD_LABEL)
        ]

        byte_code = ByteCode()
        byte_code.output = output
        return byte_code

# expects x in 0 register
class LapshaLoadSlow(IExpandable):
    # register where "x" value is stored
    X_REGISTER = 0

    def expand(self):
        # construct body
        output = [Label(LAPSHA_LOAD_LABEL)]

        for i in xrange(P2LConfig.MAX_LAPSHA_INDEX):
            if_true = LABEL_PROVIDER.next_any_label('true')
            if_false = LABEL_PROVIDER.next_any_label('false')

            value_to_compare = i
            body = [
                LoadEnv(0, self.X_REGISTER),
                LoadConstant(value_to_compare),
                CompareEqual(),
                IfBranchLabel(if_true, if_false),
                Label(if_true),
                LoadEnv(0, value_to_compare),
                ReturnFromBranch(),
                Label(if_false)
            ]
            output += body

        byte_code = ByteCode()
        byte_code.output = output
        return byte_code

# expects x in 0 register
class LapshaLoadImplementation(IExpandable):
    # register where "x" value is stored
    X_REGISTER = 0

    def dp(self, length, add):
        assert length > 0
        if length == 1:
            # x == add
            output = [
                LoadEnv(0, add),
                ReturnFromBranch(),
            ]
            return output

        if_true = LABEL_PROVIDER.next_any_label('true')
        if_false = LABEL_PROVIDER.next_any_label('false')

        mid = length / 2
        if_output = self.dp(mid, add + mid)
        else_output = self.dp(mid, add)
        output = [
            LoadEnv(0, self.X_REGISTER),
            LoadConstant(add + mid),
            CompareGreaterOrEqual(),
            IfBranchLabel(if_true, if_false),
            Label(if_true)
        ] + if_output + [
            Label(if_false)
        ] + else_output
        return output

    def expand(self):
        # construct body
        output = [Label(LAPSHA_LOAD_LABEL)]
        output += self.dp(P2LConfig.MAX_LAPSHA_INDEX, 0)
        byte_code = ByteCode()
        byte_code.output = output
        return byte_code



# executing of expansion of this byte code have following effect:
# [x, y]
# stack --> get(y)
# stack --> get(x)
# frame[n][x] = y
class SaveToEnvGeneric(IExpandable):
    def __init__(self, n):
        if n != 0:
            raise CompilationError(
                'LoadSaveGeneric is only supported from 0 frame')
        self.n = n

    def __repr__(self):
        return 'SaveToEnvGeneric({})'.format(
                self.n,
            )

    def expand(self):
        x_register = LapshaSaveImplementation.X_REGISTER
        y_register = LapshaSaveImplementation.Y_REGISTER
        output = [
            StoreToEnv(self.n, y_register),
            StoreToEnv(self.n, x_register),
            UnconditionalJumpLabelSEL(LAPSHA_SAVE_LABEL)
        ]

        byte_code = ByteCode()
        byte_code.output = output
        return byte_code



# NOTE: there is only small difference
# with Load
# expects x in 0 register
# expects y in 1 register
class LapshaSaveSlow(IExpandable):
    # register where "x" value is stored
    X_REGISTER = 0
    Y_REGISTER = 1

    def expand(self):
        # construct body
        output = [Label(LAPSHA_SAVE_LABEL)]

        for i in xrange(P2LConfig.MAX_LAPSHA_INDEX):
            if_true = LABEL_PROVIDER.next_any_label('true')
            if_false = LABEL_PROVIDER.next_any_label('false')

            value_to_compare = i
            body = [
                LoadEnv(0, self.X_REGISTER), # frame[x] --> stack
                LoadConstant(value_to_compare),
                CompareEqual(),
                IfBranchLabel(if_true, if_false),
                Label(if_true), # x == value
                # seems like: the only difference is here
                LoadEnv(0, self.Y_REGISTER), # frame[y] --> stack
                SaveToEnv(0, value_to_compare), # stack --> frame[x]
                # ^^^^
                ReturnFromBranch(),
                Label(if_false)
            ]
            output += body

        byte_code = ByteCode()
        byte_code.output = output
        return byte_code

# NOTE: there is only small difference
# with Load
# expects x in 0 register
# expects y in 1 register
class LapshaSaveImplementation(IExpandable):
    # register where "x" value is stored
    X_REGISTER = 0
    Y_REGISTER = 1

    def dp(self, length, add):
        assert length > 0
        if length == 1:
            # x == add
            output = [
                # LoadConstant(add),
                # DebugPrint(),
                LoadEnv(0, self.Y_REGISTER), # frame[y] --> stack
                SaveToEnv(0, add), # stack --> frame[x]
                ReturnFromBranch(),
            ]
            return output

        if_true = LABEL_PROVIDER.next_any_label('true')
        if_false = LABEL_PROVIDER.next_any_label('false')

        mid = length / 2
        if_output = self.dp(mid, add + mid)
        else_output = self.dp(mid, add)
        output = [
            # LoadConstant(add),
            # LoadConstant(add + length),
            # AllocateCons(),
            # DebugPrint(),
            LoadEnv(0, self.X_REGISTER),
            LoadConstant(add + mid),
            CompareGreaterOrEqual(),
            IfBranchLabel(if_true, if_false),
            Label(if_true),
        ] + if_output + [
            Label(if_false)
        ] + else_output
        return output

    def expand(self):
        # construct body
        output = [Label(LAPSHA_SAVE_LABEL)]
        # output += [
        #     LoadConstant(777),
        #     LoadEnv(0, 0),
        #     AllocateCons(),
        #     DebugPrint()
        # ]
        output += self.dp(P2LConfig.MAX_LAPSHA_INDEX, 0)
        byte_code = ByteCode()
        byte_code.output = output
        return byte_code


# TSEL - based
class UnconditionalJumpLabel(IExpandable):
    def __init__(self, label):
        self.label = label

    def expand(self):
        byte_code = ByteCode()
        byte_code.output = [
            LoadConstant(0),
            JumpLabel(self.label)
        ]
        return byte_code

#SEL - based
class UnconditionalJumpLabelSEL(IExpandable):
    def __init__(self, label):
        self.label = label

    def expand(self):
        byte_code = ByteCode()
        byte_code.output = [
            LoadConstant(0),
            JumpLabelSEL(self.label)
        ]
        return byte_code


class Label:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '{}: '.format(self.label)

class WithLabelAbstractOp:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '{} ({})'.format(self.__class__, self.label)

    # this method is used to replace label based jumps
    # with their absoulte values
    @staticmethod
    def transform(address):
        assert False

class WithLabelAbstractOp2:
    def __init__(self, label1, label2):
        self.label1 = label1
        self.label2 = label2

    def __repr__(self):
        return '{} ({}, {})'.format(
            self.__class__,
            self.label1,
            self.label2
        )

# always should be put
# with LoadConstant
class JumpLabel(WithLabelAbstractOp):
    # virtual
    @staticmethod
    def transform(address):
        return TailCallBranch(address, address)

# SEL based
class JumpLabelSEL(WithLabelAbstractOp):
    # virtual
    @staticmethod
    def transform(address):
        return ConditionalBranch(address, address)

class LoadFunctionLabel(WithLabelAbstractOp):
    # virtual
    @staticmethod
    def transform(address):
        return LoadFunction(address)

# TSEL based
class IfBranchLabel(WithLabelAbstractOp2):
    # virtual
    @staticmethod
    def transform(address1, address2):
        return TailCallBranch(address1, address2)

