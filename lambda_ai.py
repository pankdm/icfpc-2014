from emulator import *
from lambdaman_algo.smart_algo_implementation import main as algo_main
from world_converter import *
from util import *
from p2l_compiler import *
from lisp import VM

from unittest import TestCase
# dummy test case, just to use nice assertions from python unittest lib
t = TestCase("__str__")


def convert_to_vm(data):
    if isinstance(data, int):
        return VmInteger(data)
    if isinstance(data, tuple):
        t.assertTrue(len(data) >= 2)
        first = convert_to_vm(data[0])
        if len(data) == 2:
            second = convert_to_vm(data[1])
            return VmCons(first, second)
        else:
            other = convert_to_vm(data[1:])
            return VmCons(first, other)

    if isinstance(data, list):
        t.assertTrue(len(data) >= 1)
        first = convert_to_vm(data[0])
        if len(data) == 1:
            return VmCons(first, VmInteger(0))
        else:
            other = convert_to_vm(data[1:])
            return VmCons(first, other)

    if data is None:
        return VmCons(VmInteger(-1), VmInteger(-1))

    assert False, "Unknown type: {}".format(repr(data))


class LambdaManAI(AI): 
    def get_next_move(self, ai_state, world_state):
        return algo_main(ai_state, convert_world(world_state))[1]

# TODO: think about uniting with
# VM, Lisp and VmExecutor
class VmAIExecutor:
    def __init__(self, byte_code):
        self.vm = VM()
        self.byte_code = byte_code.output
        # self.expected_output = output
        self.step = 0
        self.debug_output = False

        # self.values_checked = 0

    def next_step(self):
        index = self.vm.counter
        op = self.byte_code[index]
        # print 'Executing mutate on {}'.format(repr(op))
        op.mutate(self.vm)
        self.step += 1

    def run(self):
        try:
            while (True):
                self.next_step()
        except StopExecution:
            self.message = 'Execution was stopped after {} steps'.format(
                self.step)
        except:
            print 'Unexpected error: ', sys.exc_info()[0]
            self.vm.dump()
            raise
            # self.check_all()
            # self.dump()

class LowLevelAI(AI):
    def __init__(self, algo_path):
        code = read_code(algo_path)
        p2l = P2LCompiler()
        p2l.use_submit_mode = True
        self.byte_code = p2l.compile_expr(code)
        self.message = "Just started"
        # call step function
        # self.byte_code.append( CallFunction(2) )

    def get_next_move(self, ai_state, world_state):
        executor = VmAIExecutor(self.byte_code)
        world_converted = convert_world(world_state)
        # converted_world --> actual data on the stack
        # print world_converted
        vm_world = convert_to_vm(world_converted)
        # print vm_world

        print self.message

        # fill data structures
        # input_params = VmCons(
        #     VmInteger(0), # ai_state
        #     vm_world) # world_state
        executor.vm.data_stack.append(VmInteger(0)) # ai_state
        executor.vm.data_stack.append(vm_world) # world_state
        executor.run()

        self.message = executor.message

        return_value =  executor.vm.data_stack[-1]
        # print 'Return value = ', return_value
        assert_type(return_value, VmCons)
        direction = return_value.second
        assert_type(direction, VmInteger)
        return direction.n


class CheckingAI(AI):
    def __init__(self, algo_path):
        self.low_level_ai = LowLevelAI(algo_path)
        self.python_ai = LambdaManAI()

    def get_next_move(self, ai_state, world_state):
        python_move = self.python_ai.get_next_move(
                ai_state, world_state)
        low_level_move = self.low_level_ai.get_next_move(
                ai_state, world_state)

        t.assertEquals(python_move, low_level_move)
        return python_move

def main():
    print convert_to_vm( (1, 2, 3) )
    print convert_to_vm( [1, 2, 3] )

if __name__ == '__main__':
    main()


