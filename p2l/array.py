# API:
 # by default it is initalized with zeros
# a = ALLOCATE_ARRAY(size)
#
# SET_ARRAY_VALUE(a, index, value)
# GET_ARRAY_VALUE(a, index)

# TODO:
# 1) check that next local variables allocated properly
#

def foo():
    ALLOCATE_ARRAY(a, 15)
    SET_ARRAY_VALUE(a, 0, 13)
    SET_ARRAY_VALUE(a, 1, 2)
    SET_ARRAY_VALUE(a, 5, 8)

    x1 = GET_ARRAY_VALUE(a, 0)
    x2 = GET_ARRAY_VALUE(a, 1)
    x3 = GET_ARRAY_VALUE(a, 5)

    PRINT( (x1, x2, x3) )
    b = GET_ARRAY_VALUE(a, 1) + GET_ARRAY_VALUE(a, 5)
    c = GET_ARRAY_VALUE(a, 0) + GET_ARRAY_VALUE(a, 1)
    d = GET_ARRAY_VALUE(a, 0) + GET_ARRAY_VALUE(a, 1) + GET_ARRAY_VALUE(a, 5)
    PRINT(b)
    PRINT(c)
    PRINT(d)
    PRINT( GET_ARRAY_VALUE(a, 10) )

foo()

# prints:
# (13, (2, 8))
# 10
# 15
# 23
# 0
