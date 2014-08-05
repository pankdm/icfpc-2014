
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


# Implementations of shared functions
from python_stl import *

def centerize(xy, cxy):
    x = FIRST(xy) - FIRST(cxy) + HALF_WINDOW_SIZE
    y = SECOND(xy) - SECOND(cxy) + HALF_WINDOW_SIZE
    return (x, y)

def get_location(xy, direction):
    moves = ((0, -1), (1, 0), (0, 1),  (-1, 0), (0, 0))
    move = GET_VALUE(moves, direction)
    return (FIRST(xy) + FIRST(move), SECOND(xy) + SECOND(move))

def valid_location(world, xy):
    return not (GET_WORLD(world, xy) == WALL)

def next_direction(direction):
    direction = direction + 1
    if direction == 4:
        direction = 0
    return direction

def from_2d(x, y):
    return WINDOW_SIZE * y + x

def from_2d_pair(xy):
    return WINDOW_SIZE * SECOND(xy) + FIRST(xy)

def from_2d_pair_centered(xy, cxy):
    true_xy = centerize(xy, cxy)
    return WINDOW_SIZE * SECOND(true_xy) + FIRST(true_xy)


def foo(iterations):
    while iterations > 0:
        PRINT(iterations)
        iterations = iterations - 1

foo(5)

# prints:
# 5
# 4
# 3
# 2
# 1
