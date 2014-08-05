def foo(a, b, c):
    return a == b and b == c

PRINT(foo(1, 1, 1))
PRINT(foo(2, 1, 1))
PRINT(foo(2, 2, 1))
PRINT(foo(1, 2, 2))
PRINT(foo(2, 2, 2))

# Prints
# 1
# 0
# 0
# 0
# 1
