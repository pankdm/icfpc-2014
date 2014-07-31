from astpp import *
import ast

import sys

from instructions import *
from p2l_internals import *
from p2l_visitor import P2LVisitor
from p2l_supported import *
from p2l_labels import *

def read_code(file_name):
    f = open(file_name, 'rt')
    code = ''.join(f.readlines())
    return code

def write_to_file(file_name, code):
    f = open(file_name, 'wt')
    f.write(code)
    f.close()


class P2LCompiler:
    def __init__(self):
        self.functions = []

        # some definitions that will be prepeneded
        # to main definitios
        self.precompiled_code = ByteCode()

        # stack of local variables
        # we start with empty variables

        main_scope = ScopeVariables()
        # in the main frame we don't have allocated registers
        # main_scope.free_index = 0

        self.local_vars_stack = [ main_scope ]

        self.global_vars = {}
        self.global_vars_values = {}

        # settings
        self.use_submit_mode = False
        self.use_standard_library = True
        self.WORK_DIR = 'p2l_workdir'

    def local_vars(self):
        return self.local_vars_stack[-1]

    def add_precompiled_code(self):
        # currently we are adding on lapsha-type functions
        output = [
            LapshaLoadImplementation(),
            LapshaSaveImplementation(),
        ]

        self.precompiled_code = ByteCode.from_list(output)


    def include_constants(self):
        # process file with constants and add them to
        # global vars
        visitor = P2LVisitor(self)
        visitor.process_consts = True

        code = read_code('include/consts.py')
        tree = ast.parse(code)
        visitor.visit(tree)

    @staticmethod
    def with_standard_library(code):
        stl_code = read_code('include/stl.py')
        common_code = read_code('include/common.py')
        return '{}\n\n{}\n\n{}'.format(stl_code, common_code, code)

    def compile_source_code(self, source_code):
        tree = ast.parse(source_code)

        # here only outer body is translated to byte_code
        # all declarations are parsed in internal compiler
        # structures
        byte_code = P2LVisitor(self).visit(tree)
        result = self.postprocess_byte_code(byte_code)
        return result

    def compile_expr(self, code):
        if self.use_standard_library:
            code = P2LCompiler.with_standard_library(code)

        write_to_file('p2l_workdir/input_with_stl.py', code)

        self.include_constants()
        self.add_precompiled_code()
        return self.compile_source_code(code)

    def postprocess_byte_code(self, byte_code):
        # byte_code.show_without_source()
        filtered_code = self.filter_empty_codes(byte_code)
        with_main = self.add_main(byte_code)
        expanded_code = self.expand_byte_code(with_main)

        write_to_file(
            'p2l_workdir/with_labels.gcc',
            expanded_code.dump_without_source())

        code_without_labels = self.replace_labels(expanded_code)
        return code_without_labels

    def search_function(self, func_name):
        # check already defined functions
        for f in self.functions:
            if f.name == func_name:
                return ApplyFunction(func_name, f.arity, f.dummy_arity)

        function = search_in_builtin(func_name)
        if function:
            print 'Found "{}" in built-in functions'.format(
                func_name)
            return function

        if function == None:
            raise CompilationError('Unknown function "{}"'.format(func_name))

    def filter_empty_codes(self, byte_code):
        result = ByteCode()
        for op in byte_code.output:
            if not isinstance(op, EmptyByteCode):
                result.append(op)
        return result

    def add_main(self, byte_code):
        result = ByteCode()

        if self.use_submit_mode:
            result.append( LoadConstant(0) )
            result.append( LoadFunctionLabel('main') )
            result.append( AllocateCons() )
            result.append( ReturnFromFunction() )
        else:
            result.append( LoadConstant(0) )
            result.append( JumpLabel(MAIN_LABEL) )

        # add precompiled code:
        result.append_byte_code( self.precompiled_code )

        # add function definitions
        for impl in self.functions:
            result.output += [ Label(impl.name) ]
            result.append_byte_code( impl.byte_code )


        if self.use_submit_mode:
            # assert len(byte_code.output) == 0
            pass
        else:
            result.append( Label(MAIN_LABEL) )
            result.append_byte_code( byte_code )

        return result


    def expand_byte_code(self, main_byte_code):
        print
        print 'This code before expansion:'
        main_byte_code.show_without_source()

        # iterate on expansion until all operands are expanded
        it = 0
        while (True):
            print 'Expansion iteration, ', it
            result = ByteCode()
            no_changes = True
            for op in main_byte_code.output:
                if isinstance(op, IExpandable):
                    # here we need to expand operand
                    expanded_byte_code = op.expand()
                    print 'Expanding ', op
                    result.append_byte_code(expanded_byte_code)
                    no_changes = False
                else:
                    result.append(op)
            main_byte_code = result
            it += 1
            if no_changes: break

        print
        print 'This code was expanded:'
        main_byte_code.show_without_source()
        return main_byte_code

    # changes byte_code in place
    def replace_labels(self, byte_code):
        output = byte_code.output

        # gather addresses
        labels_addresses = {}
        index = 0
        for op in output:
            if isinstance(op, Label):
                labels_addresses[op.label] = index
            else:
                index += 1

        # replace labels
        result = ByteCode()
        index = 0
        for op in output:
            if not isinstance(op, Label):
                if isinstance(op, WithLabelAbstractOp):
                    label = op.label
                    # print op
                    address = labels_addresses[label]
                    new_op = op.transform(address)
                    result.append(new_op)
                elif isinstance(op, WithLabelAbstractOp2):
                    label1 = op.label1
                    label2 = op.label2

                    address1 = labels_addresses[label1]
                    address2 = labels_addresses[label2]
                    new_op = op.transform(address1, address2)
                    result.append(new_op)
                else:
                    result.append(op)

        # print
        # print 'After replacing:'
        # result.show_without_source()
        return result


def main():
    if len(sys.argv) > 1:
        code = read_code(sys.argv[1])
    else:
        code = read_code('p2l/1.lisp.py')
    # parseprint(code)
    # dump syntax tree to file
    write_to_file('p2l_workdir/syntax_tree.py', dump(parse(code)))
    write_to_file('p2l_workdir/input.py', code)

    p2l = P2LCompiler()
    # p2l.use_submit_mode = True
    # p2l.use_standard_library = False

    byte_code = p2l.compile_expr(code)
    # print
    # byte_code.show_without_source()

    # print 'Source:'
    # print byte_code.to_source()
    write_to_file('p2l_workdir/submit.gcc', byte_code.to_source())

    print
    print 'OK'

if __name__ == '__main__':
    main()

