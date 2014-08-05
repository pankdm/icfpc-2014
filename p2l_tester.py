
import sys
from p2l_compiler import P2LCompiler
from util import *
from astpp import *

from lisp import VM
from instructions import *

from unittest import TestCase
# dummy test case, just to use nice assertions from python unittest lib
t = TestCase("__str__")

import os

class VmExecutor:
    def __init__(self, byte_code, output):
        self.vm = VM()
        self.byte_code = byte_code.output
        self.expected_output = output
        self.step = 0
        self.debug_output = False

        self.values_checked = 0

    def run(self):
        self.debug_output = False
        try:
            while (True):
                self.next_step()
        except StopExecution:
            print 'Execution was stopped'
            self.check_all()
            # self.dump()
    
    def check_all(self):
        vm = self.vm
        self.check( vm.data_stack == [] )
        self.check( vm.control_stack == [] )
        t.assertEqual(
            len(self.expected_output),
            len(vm.trace_output))
        for i in xrange(len(self.expected_output)):
            left = self.expected_output[i]
            right = vm.trace_output[i]
            t.assertEquals(str(left), repr(right))
            self.values_checked += 1

        print 'OK, checked:', self.values_checked

    def check(self, condition):
        if not condition:
            self.dump()
            assert False, 'Something went wrong'

    def next_step(self):
        index = self.vm.counter
        op = self.byte_code[index]
        if self.debug_output:
            self.dump()
            print
        # line = self.program_code[index]
        # if self.debug_output:
        #     print 'address =', self.vm.counter
        # print 'Executing mutate on {} ("{}")'.format(repr(op), line)
        op.mutate(self.vm)
        self.step += 1

    def dump(self):
        print
        print
        print 'step = ', self.step
        self.vm.dump()


class P2LTester:
    def __init__(self):
        pass

    def extract_expected_output(self, code):
        result = []
        start = False
        for line in code.split('\n'):            
            # consider only comments
            if not line.startswith('#'):
                continue
            lower_line = line.lower()
            if start:
                value = lower_line.replace('#', ' ')
                result.append(eval(value))

            if 'prints' in lower_line:
                start = True

        print 'Found', result
        return result

    def check_output(self, byte_code, output):
        executor = VmExecutor(byte_code, output)
        executor.run()

    def test_file(self, file_name):
        print
        print 'Testing', file_name
        code = read_code(file_name)

        only_name = file_name.split('/')[-1]

        p2l = P2LCompiler()
        p2l.WORK_DIR = 'testing-output'
        
        byte_code = p2l.compile_expr(code)
        p2l.save_in_work_dir('submit.gcc', byte_code.to_source())

        output = self.extract_expected_output(code)
        self.check_output(byte_code, output)

def main():
    if sys.argv[1] == 'dir':
        # test whole directory
        directory = sys.argv[2]


        skip = False

        start = None
        if len(sys.argv) >= 4:
            print 'init skip'
            skip = True
            start = sys.argv[3]

        for f in os.listdir(directory):
            if 'unsupported' in f:
                print
                print 'UNSUPPORTED: ', f
                continue

            if start == f:
                skip = False
            
            if skip:
                print 
                print 'SKIPPING: ', f
                continue

            file_name = directory + '/' + f
            tester = P2LTester()
            tester.test_file(file_name)
    else:
        file_name = sys.argv[1]
        tester = P2LTester()
        tester.test_file(file_name)

    print
    print 'OK'

if __name__ == '__main__':
    main()

