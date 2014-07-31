from include.python_stl import *
from include.common import *
import random
import math


def main_implementation(ai_state, world_state):
    # Just world
    world = GET_VALUE(world_state, 0)
    # Tupple vitality, (x,y), direction, lives, score.
    man = GET_VALUE(world_state, 1)
    man_location = GET_VALUE(man, 1)
    man_direction = GET_VALUE(man, 2)
    # List of ghost. Ghost - vitality, (x,y), direction.
    ghosts = GET_VALUE(world_state, 2)
    # Presense of a fruit.
    # fruit = GET_VALUE(world_state, 3)

    final_direction = man_direction
    valid_directions = 0
    iteration = 0
    while iteration < 4:
        PRINT(5)
        PRINT(man_location)
        new_location = get_location(man_location, iteration)
        PRINT(7)
        PRINT(new_location)
        PRINT(valid_location(world, new_location))
        if valid_location(world, new_location):
            PRINT(8)
            valid_directions = valid_directions + 1
            PRINT(6)
        iteration = iteration + 1
    PRINT(4)
    while not valid_location(world, get_location(man_location, final_direction)):
        final_direction = next_direction(final_direction)
    return (0, final_direction)

def main(ai_state, world):
    return main_implementation(ai_state, world)
