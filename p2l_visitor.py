import ast

from p2l_internals import *
from p2l_supported import *
from p2l_labels import LABEL_PROVIDER

class P2LVisitor(ast.NodeVisitor):
    def __init__(self, compiler):
        self.compiler = compiler

        # [very hacky]
        # we use this flag to distinguish between cases
        # 1) compiling main source code
        # 2) compiling global constants from "stdlib"
        self.process_consts = False

    def visit(self, node):
        # print
        # print 'Visiting', node
        byte_code = ast.NodeVisitor.visit(self, node)
        # print
        # print 'Visited', node
        # print byte_code
        # byte_code.show_without_source()
        assert isinstance(byte_code, ByteCode), str(byte_code)
        return byte_code

    def visit_FunctionDef(self, node):
        # get function parametres
        # and store them in compiler's data structures
        scope = ScopeVariables()

        # in main function of submit mode we don't have
        # any allocated registers
        # hacky!
        if self.compiler.use_submit_mode == True:
            if node.name == P2LConfig.MAIN_IN_SUBMIT_MODE:
                scope.free_index = 0

        all_args = node.args
        # iterate over positional args
        positional_args = all_args.args
        for arg in positional_args:
            arg_name = arg.id
            scope.declare_variable( arg_name, is_local=False )

        self.compiler.local_vars_stack.append(scope)

        # parse function body and add "return"
        byte_code = self.visit_expressions(node.body)
        byte_code.append( ReturnFromFunction() )

        # we store function definition in compiler
        impl = FunctionImpl(node.name, byte_code)
        impl.arity = len(positional_args)

        # scope probably was adjusted (due to local vars) so
        # we probably need to allocate more space
        total_slots = scope.total_slots_allocated()
        impl.dummy_arity = scope.dummy_slots_allocated()

        self.compiler.functions.append(impl)

        # and return empty byte_code
        return ByteCode()

    def visit_Return(self, node):
        # ignore return and just put underlying value on stack
        byte_code = self.visit(node.value)
        return byte_code


    def visit_Compare(self, node):
        assert len(node.ops) == 1
        assert len(node.comparators) == 1
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])

        # we use rewrite rule
        # a < b   < ----- >   b > a
        op = node.ops[0]
        if isinstance(op, ast.Lt):
            op = ast.Gt()
            left, right = right, left

        byte_code = ByteCode()
        byte_code.append_byte_code(left)
        byte_code.append_byte_code(right)

        compare_op = COMPARE_OPERATIONS().get_or_fail(op)
        byte_code.append(compare_op)
        return byte_code


    def visit_expressions(self, expressions):
        byte_code = ByteCode()
        for expr in expressions:
            next = self.visit(expr)
            byte_code.output += next.output
        return byte_code

    def visit_If(self, node):
        condition = self.visit(node.test)
        if_branch = self.visit_expressions(node.body)
        else_branch = self.visit_expressions(node.orelse)

        true_label = LABEL_PROVIDER.next_if_label('true')
        false_label = LABEL_PROVIDER.next_if_label('false')
        finish_label = LABEL_PROVIDER.next_if_label('finish')

        byte_code = ByteCode()
        byte_code.append_byte_code( condition )
        byte_code.append(
            IfBranchLabel(true_label, false_label)
        )

        # if body
        byte_code.append( Label(true_label) )
        byte_code.append_byte_code( if_branch )

        byte_code.append( LoadConstant(0) )
        byte_code.append( JumpLabel(finish_label) )

        # else body
        byte_code.append( Label(false_label) )
        byte_code.append_byte_code( else_branch )

        # continuation
        byte_code.append( Label(finish_label) )
        return byte_code

    def visit_Name(self, node):
        name = node.id
        scope = self.compiler.local_vars()
        global_vars = self.compiler.global_vars

        byte_code = scope.produce_get_byte_code(name)

        if name in global_vars:
            byte_code = ByteCode()
            byte_code.append_byte_code( global_vars[name] )

        if not byte_code:
            raise CompilationError(
                'Unknown variable "{}"'.format(name))
        return byte_code

    def visit_ImportFrom(self, node):
        # Ignore
        return EmptyByteCode()

    def visit_Import(self, node):
        # Ignore
        return EmptyByteCode()

    def visit_Tuple(self, node):
        byte_code = ByteCode()

        for element in node.elts:
            element_code = self.visit(element)
            byte_code.append_byte_code(element_code)

        # combine CONS appropriate number of times
        # compare to list:
        # here we don't have ending 0
        for i in xrange(len(node.elts) - 1):
            byte_code.append( AllocateCons() )

        return byte_code

    def visit_List(self, node):
        byte_code = ByteCode()

        for element in node.elts:
            element_code = self.visit(element)
            byte_code.append_byte_code(element_code)

        byte_code.append( LoadConstant(0) )
        # combine CONS appropriate number of times
        for i in xrange(len(node.elts)):
            byte_code.append( AllocateCons() )

        return byte_code


    def visit_Module(self, node):
        byte_code = ByteCode()
        for expr in node.body:
            next = self.visit(expr)
            byte_code.output += next.output
        byte_code.append( ReturnFromFunction() )
        return byte_code

    def visit_While(self, node):
        condition = self.visit(node.test)
        body = self.visit_expressions(node.body)

        while_label = LABEL_PROVIDER.next_while_label('start')
        body_label = LABEL_PROVIDER.next_while_label('body')
        finish_label = LABEL_PROVIDER.next_while_label('finish')

        byte_code = ByteCode()

        byte_code.append( Label(while_label) )
        byte_code.append_byte_code( condition )
        byte_code.append(
            IfBranchLabel(body_label, finish_label)
        )

        # while body
        byte_code.append( Label(body_label) )
        byte_code.append_byte_code( body )

        # jump on iteration
        byte_code.append( LoadConstant(0) )
        byte_code.append( JumpLabel(while_label) )

        # exit of while
        byte_code.append( Label(finish_label) )
        return byte_code


    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        func_name = node.func.id

        # special functions
        if func_name == 'ALLOCATE_ARRAY':
            args = node.args
            assert len(args) == 2
            assert_type(args[0], ast.Name)

            size_arg = args[1]
            # HACKING IT:
            if isinstance(size_arg, ast.Num):
                size = args[1].n
            elif isinstance(size_arg, ast.Name):
                constant_name = size_arg.id
                size = self.compiler.global_vars_values[constant_name]
            else:
                raise CompilationError(
                    'Unknown type of 2nd argument in ALLOCATE_ARRAY'.format(
                        str(size_arg)
                ))

            name = args[0].id
            scope = self.compiler.local_vars()
            scope.declare_array(name, size)
            return ByteCode()

        if func_name == 'GET_ARRAY_VALUE':
            args = node.args
            assert len(args) == 2
            assert_type(args[0], ast.Name)

            name = args[0].id
            scope = self.compiler.local_vars()
            offset = scope.array_offset(name)

            output = []
            next = self.visit(args[1])


            output += next.output
            output += [
                LoadConstant(offset),
                IntAddition(),
                LoadEnvGeneric(0)
            ]
            return ByteCode.from_list(output)

        if func_name == 'SET_ARRAY_VALUE':
            args = node.args
            assert len(args) == 3
            assert_type(args[0], ast.Name)

            name = args[0].id
            scope = self.compiler.local_vars()
            offset = scope.array_offset(name)

            output = []

            # parse params
            x_param = self.visit(args[1])
            y_param = self.visit(args[2])

            # we need to add byte code for incrementing offset
            output += x_param.output
            output += [
                LoadConstant(offset),
                IntAddition()
            ]

            output += y_param.output
            output += [
                SaveToEnvGeneric(0)
            ]
            return ByteCode.from_list(output)

        # usual path

        byte_code = ByteCode()
        output = []

        # allocate registers
        if func_name not in BUILTIN_FUNCTIONS:
            # we don't need to allocate for builtin functions
            for i in xrange(P2LConfig.NUM_REGISTERS):
                output.append( LoadConstant(0) )

        for arg in node.args:
            next = self.visit(arg)
            output += next.output

        function = self.compiler.search_function(func_name)
        output.append(function)

        return ByteCode.from_list(output)

    def visit_Assign(self, node):
        assert len(node.targets) == 1
        var_name = node.targets[0].id

        right = self.visit(node.value)

        byte_code = ByteCode()
        byte_code.append_byte_code( right )

        scope = self.compiler.local_vars()

        # TODO: refactor
        # check if variable is already defined
        if scope.is_declared(var_name):
            assign = scope.produce_assign_byte_code(var_name)
            byte_code.append_byte_code( assign )
        else:
            # print 'Need to alocate', var_name
            # allocate new space for variable
            if self.process_consts:
                # add to global array
                # very hacky!
                global_vars = self.compiler.global_vars
                global_vars[var_name] = byte_code

                # also add constants to global
                assert_type(node.value, ast.Num)
                global_vars_values = self.compiler.global_vars_values
                global_vars_values[var_name] = node.value.n
            else:
                scope.declare_variable(var_name, is_local=True)
                assign = scope.produce_assign_byte_code(var_name)
                byte_code.append_byte_code( assign )

        return byte_code

    def visit_UnaryOp(self, node):
        # only nots are supported currently
        assert_type(node.op, ast.Not)

        next = self.visit(node.operand)

        # rewrite rule:
        # not x   <--->   x == 0
        byte_code = ByteCode()
        byte_code.append_byte_code(next)
        byte_code.append( LoadConstant(0) )
        byte_code.append( CompareEqual() )

        return byte_code

    def visit_BoolOp(self, node):
        # only ands are supported currently
        assert_type(node.op, ast.And)
        assert (len(node.values) == 2)

        output = []
        left = self.visit(node.values[0])
        right = self.visit(node.values[1])

        output += left.output
        output += right.output
        # rewrite rule:
        # X and Y  <----> X + Y == 2
        output += [
            IntAddition(),
            LoadConstant(2),
            CompareEqual()
        ]
        return ByteCode.from_list(output)


    def visit_BinOp(self, node):
        # print 'At BinOp', node.op

        byte_code = ByteCode()
        left = self.visit(node.left)
        right = self.visit(node.right)

        byte_code.output += left.output
        byte_code.output += right.output

        binary_op = BINARY_OPERATIONS().get_or_fail(node.op)
        byte_code.append(binary_op)
        # self.generic_visit(node)
        return byte_code

    def visit_Num(self, node):
        byte_code = ByteCode()
        byte_code.append( LoadConstant(node.n) )
        return byte_code

