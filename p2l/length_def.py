

def LENGTH(x):
    size = 0
    while not ATOM(x):
        x = SECOND(x)
        size = size + 1
    return size

PRINT(LENGTH([1, 2, 3, 4]))
PRINT(LENGTH([1]))
PRINT(LENGTH([]))

# Expected:
# 4
# 1
# 0
