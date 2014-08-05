

def LENGTH1(x):
    size = 0
    while not ATOM(x):
        x = SECOND(x)
        size = size + 1
    return size

PRINT(LENGTH1([1, 2, 3, 4]))
PRINT(LENGTH1([1]))
PRINT(LENGTH1([]))

# prints:
# 4
# 1
# 0
