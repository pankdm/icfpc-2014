from include.python_stl import *
from include.common import *
import random
import math

def valid_location_centered(world, xy, cxy):
    true_xy = centerize(xy, cxy)
    result = 0
    if (((FIRST(true_xy) >= 0 and\
            FIRST(true_xy) < WINDOW_SIZE) and\
            SECOND(true_xy) >= 0) and\
            SECOND(true_xy) < WINDOW_SIZE):
        if not GET_WORLD(world, xy) == WALL:
            result = 1
    return result

def get_cost(value, distance):
    result = 0
    if value == PILL:
        result = (distance + 1)
    if value == POWER_PILL:
        result = (distance + 1)
    return result


def calculate_cost(world, location, vitality, ghosts, fruit):
    ALLOCATE_ARRAY(distance, ARRAY_SIZE)
    ALLOCATE_ARRAY(queue, ARRAY_SIZE)
    x = 0
    y = 0
    while x < WINDOW_SIZE:
        y = 0
        while y < WINDOW_SIZE:
            SET_ARRAY_VALUE(distance, from_2d(x, y), INF) 
            y = y + 1
        x = x + 1

    fruit_location = (INF, INF)
    cell = GET_WORLD(world, location)
    if cell == FRUIT:
        fruit_location = location


    # Handling world
    SET_ARRAY_VALUE(queue, 0, location)
    SET_ARRAY_VALUE(distance, from_2d_pair_centered(location, location), 0)

    cost = get_cost(cell, 0)
    min_cost = INF
    if not cost == 0:
        min_cost = cost

    id = 0
    total = 1
    while id < total:
        current_location = GET_ARRAY_VALUE(queue, id)
        new_distance = GET_ARRAY_VALUE(distance, from_2d_pair_centered(current_location, location)) + 1
        id = id + 1
        direction = 0
        while direction < 4:
            new_location = get_location(current_location, direction)
            new_location_id = from_2d_pair_centered(new_location, location)
            if valid_location_centered(world, new_location, location):
                if GET_ARRAY_VALUE(distance, new_location_id) > new_distance:
                    SET_ARRAY_VALUE(distance, new_location_id, new_distance)
                    cell = GET_WORLD(world, new_location)
                    if cell == FRUIT:
                        fruit_location = new_location
                    cur_cost = get_cost(cell, new_distance)
                    cost = cost + cur_cost
                    if cur_cost > 0 and cur_cost < min_cost:
                        min_cost = cur_cost
                    SET_ARRAY_VALUE(queue, total, new_location)
                    total = total + 1
            direction = direction + 1
    if min_cost == 0:
        min_cost = 1

    # Handling ghosts
    min_ghost = INF
    id = 0
    total = LENGTH(ghosts)
    while id < total:
        ghost = GET_VALUE(ghosts, id)
        if not GET_VALUE(ghost, 0) == 2 and valid_location_centered(world, GET_VALUE(ghost, 1), location):
            ghost_dist = GET_ARRAY_VALUE(distance, from_2d_pair_centered(GET_VALUE(ghost, 1), location))
            if ghost_dist < min_ghost:
                min_ghost = ghost_dist
        id = id + 1

    if min_ghost == 0:
        min_ghost = 1
    if min_ghost > 15:
        min_ghost = INF


    cost = cost - 160000 / (min_cost + 1)
    if vitality > 127 * (min_ghost + 1):
        cost = cost - 600000 / min_ghost
    else:
        if min_ghost < 6:
            cost = cost + 250000 / min_ghost
    
    # Handling fruit
    if valid_location_centered(world, fruit_location, location):
        fruit_distance = GET_ARRAY_VALUE(distance, from_2d_pair_centered(fruit_location, location))
        if fruit > 127 * fruit_distance:
            cost = cost - 190000 / (fruit_distance + 1)

    return cost

def main_implementation(ai_state, world_state):
    # Just world
    world = GET_VALUE(world_state, 0)
    # Tupple vitality, (x,y), direction, lives, score.
    man = GET_VALUE(world_state, 1)
    man_vitality = GET_VALUE(man, 0)
    man_location = GET_VALUE(man, 1)
    man_direction = GET_VALUE(man, 2)
    # List of ghost. Ghost - vitality, (x,y), direction.
    ghosts = GET_VALUE(world_state, 2)
    # Presense of a fruit.
    fruit = GET_VALUE_TERMINAL(world_state, 3)

    best_direction = man_direction#random.randint(0, 3)
    best_cost = INF

    iteration = 0
    direction = man_direction
    while iteration < 4:
        new_location = get_location(man_location, direction)
        if valid_location(world, new_location):
            # We're lossing some of the information here for now
            cost = calculate_cost(world, new_location, man_vitality, ghosts, fruit)
            if cost < best_cost:
                best_cost = cost
                best_direction = direction
        direction = direction + 1
        if direction == 4:
            direction = 0
        iteration = iteration + 1
    return (0, best_direction)

def main(ai_state, world):
    return main_implementation(ai_state, world)
