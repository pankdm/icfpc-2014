def bar(x, y):
    ALLOCATE_ARRAY(array, ARRAY_SIZE)
    SET_ARRAY_VALUE(array, x, y)
    y = GET_ARRAY_VALUE(array, x)
    PRINT(y)
    return y

def foo():
    x = 777 + bar(3, 20)
    PRINT(x)

foo()

# prints:
# 20
# 797
