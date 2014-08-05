def GET_VALUE(tup, idx):
    while idx > 0:
        tup = SECOND(tup)
        idx = idx - 1
    return FIRST(tup)


def GET_ARRAY(a, xy):
    return GET_VALUE(GET_VALUE(a, FIRST(xy)), SECOND(xy))

def GET_LOCATION(xy, direction):
    moves = ((-1, 0), (0, 1), (1, 0), (0, -1), (0, 0))
    move = GET_VALUE(moves, direction)
    return (FIRST(current_location) + FIRST(move), SECOND(current_location) + SECOND(move))


def valid_location(world, xy):
    return GET_ARRAY(world, xy) != '#'

def move(ai_state, world_state):
    # Just world
    world = GET_VALUE(world_state, 0)
    # Tupple vitality, (x,y), direction, lives, score.
    man = GET_VALUE(world_state, 1)
    man_location = GET_VALUE(man, 1)
    man_direction = GET_VALUE(man, 2)
    # List of ghost. Ghost - vitality, (x,y), direction.
    ghosts = GET_VALUE(world_state, 2)
    # Presense of a fruit.
    fruit = GET_VALUE(world_state, 3)

    final_direction = man_direction

    valid_directions = 0
    iteration = 0
    while iteration < 4:
        new_location = GET_LOCATION(man_location, direction)
        if valid_location(world, new_location):
            valid_directions = valid_directions + 1
        iteration = iteration + 1

    if valid_directions > 2 or not valid_location(new_location, GET_LOCATION(man_location, man_direction)):
        while not valid_location(new_location, GET_LOCATION(man_location, final_direction)):
            final_direction = (final_direction + 1) % 4
    return final_direction
