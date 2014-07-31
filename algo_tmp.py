from emulator import *
import random
import math

moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

kInf = 1000000000

def get_new_location(current_location, direction):
    move = moves[direction]
    return (current_location[0] + move[0], current_location[1] + move[1])

def valid_location(location, world):
    size_x = len(world)
    size_y = len(world[0])
    return location[0] >= 0 and location[0] < size_x and\
        location[1] >= 0 and location[1] < size_y and\
        world[location[0]][location[1]] != '#'

def get_cost(value, distance):
    if value in ".o":
        return math.log(distance + 1)
    return 0


def calculate_cost(world, location, ghosts, fruit):
    size_x = len(world)
    size_y = len(world[0])

    distance = []
    for x in xrange(size_x):
        distance.append([kInf for y in xrange(size_y)])

    id = 0
    total = 1
    queue = [location]
    distance[location[0]][location[1]] = 0
    cost = 0.0
    while id < total:
        current_location = queue[id]
        id = id + 1
        for direction in xrange(4):
            new_location = get_new_location(current_location, direction)
            if valid_location(new_location, world):
                if distance[new_location[0]][new_location[1]] > distance[current_location[0]][current_location[1]] + 1:
                    distance[new_location[0]][new_location[1]] = distance[current_location[0]][current_location[1]] + 1
                    total = total + 1
                    cost = cost + get_cost(world[new_location[0]][new_location[1]], distance[new_location[0]][new_location[1]])
                    queue.append(new_location)
    return cost

def move(ai_state, world_state):
    # Just world
    world = world_state[0]
    # Tupple vitality, (x,y), direction, lives, score.
    man = world_state[1]
    man_location = man[1]
    # List of ghost. Ghost - vitality, (x,y), direction.
    ghosts = world_state[2]
    # Presense of a fruit.
    fruit = world_state[3]

    best_direction = 0#random.randint(0, 3)
    best_cost = kInf

    for direction in xrange(4):
        new_location = get_new_location(man_location, direction)
        if valid_location(new_location, world):
            # We're lossing some of the information here for now
            cost = calculate_cost(world, new_location, ghosts, fruit)
            if cost < best_cost:
                best_cost = cost
                best_direction = direction
                print direction, cost
    return best_direction

class LambdaManAI(AI):
    def __init__(self, world):
       self.world = world 
#def get_next_move(self):
        # Cake is a lie!
#man = (0, (self.world.man.y, self.world.man.x), 0, 0, 0)
#return self.make_move(None, (self.world.data, man, self.world.ghosts, 0))
    def get_next_move(self, ai_state, world_state):
        return move(ai_state, world_state)

def main():
    world = World()
    world.load_map_from_file('maps/world-classic.txt')

    world.set_man_ai(LambdaManAI(world))
    world.set_ghost_ai(0, RandomGhostAI())
    world.set_ghost_ai(1, RandomGhostAI())
    world.set_ghost_ai(2, RandomGhostAI())
    world.set_ghost_ai(3, RandomGhostAI())

    world.wait_after_each_turn = True
    world.run()

if __name__ == '__main__':
    main()
