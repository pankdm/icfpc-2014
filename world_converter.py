import copy
from include.python_stl import *

def convert_value(value):
    if value == '#':
        return WALL
    elif value == ' ':
        return EMPTY
    elif value == '.':
        return PILL
    elif value == 'o':
        return POWER_PILL
    elif value == '%':
        return FRUIT

def convert_world(world_state):
    new_world_state = copy.deepcopy(world_state)
    for x in xrange(len(new_world_state[0])):
        for y in xrange(len(new_world_state[0][x])):
            new_world_state[0][x][y] = convert_value(new_world_state[0][x][y])
    return new_world_state
