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
