# arrays in nexted are unsupported

def bar(x, y):
    SET_ARRAY_VALUE(array, x, y)
    return GET_ARRAY_VALUE(array, x)

def foo():
    ALLOCATE_ARRAY(array, 5)
    PRINT(bar(3, 20))


foo()

# prints:
# 20
