def get_value(tup, idx):
    while idx > 0:
        tup = SECOND(tup)
        idx = idx - 1
    FIRST(tup)

PRINT(get_value((1, 2, 3, 4, 5), 0))
PRINT(get_value((1, 2, 3, 4, 5), 2))
PRINT(get_value((1, 2, 3, 4, 5), 4))
