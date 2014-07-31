
def LENGTH(x):
    size = 0
    while not ATOM(x):
        x = SECOND(x)
        size = size + 1
    return size

def GET_VALUE_TERMINAL(tup, idx):
    while idx > 0:
        tup = SECOND(tup)
        idx = idx - 1
    return tup

def GET_VALUE(tup, idx):
    while idx > 0:
        tup = SECOND(tup)
        idx = idx - 1
    return FIRST(tup)


def GET_WORLD(a, xy):
    return GET_VALUE(GET_VALUE(a, SECOND(xy)), FIRST(xy))

def GET_LOCATION(xy, direction):
    moves = ((-1, 0), (0, 1), (1, 0), (0, -1), (0, 0))
    move = GET_VALUE(moves, direction)
    return (FIRST(xy) + FIRST(move), SECOND(xy) + SECOND(move))
