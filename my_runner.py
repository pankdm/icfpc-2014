from emulator import *
from simple_algo_implementation import *
from world_converter import *

if __name__ == '__main__':
    world = World()
    world.load_map_from_file('maps/world-classic.txt')
    world.wait_after_each_turn = len(sys.argv) > 1

    world.set_man_ai(KeyboardAI())
    world.set_ghost_ai(0, ChaseGhostAI(0))
    world.set_ghost_ai(1, RandomGhostAI(1))
    world.set_ghost_ai(2, RandomGhostAI(2))
    world.set_ghost_ai(3, RandomGhostAI(3))

    world.run()
