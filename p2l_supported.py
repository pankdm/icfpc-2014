import ast

from instructions import *
from p2l_internals import *

class SupportedOperations(object):
    def get_or_fail(self, op):
        for class_name, result in self.value.items():
            if isinstance(op, class_name):
                # should return AbstractOp type
                assert isinstance(result, AbstractOp)
                return result

        raise CompilationError(
            "Couldn't find {} in {}".format(
                    op,
                    self.__class__
            )
        )

class COMPARE_OPERATIONS(SupportedOperations):
    value = {
        ast.Gt: CompareGreater(),
        ast.GtE: CompareGreaterOrEqual(),
        ast.Eq: CompareEqual()
    }


class BINARY_OPERATIONS(SupportedOperations):
    value = {
        ast.Add: IntAddition(),
        ast.Sub: IntSubtraction(),
        ast.Mult: IntMultiplication(),
        ast.Div: IntDivision()
    }


BUILTIN_FUNCTIONS = {
    'PRINT' : DebugPrint(),
    'FIRST' : ExtractFirst(),
    'SECOND': ExtractSecond(),
    'ATOM'  : IsInteger()
}

def search_in_builtin(func_name):
    function = BUILTIN_FUNCTIONS.get(func_name, None)
    return function
