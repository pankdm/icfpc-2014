# magic spells to include files from outer dir
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from emulator import *
# from lambdaman_algo.smart_algo_implementation import *
from world_converter import *
from lambda_ai import *

if __name__ == '__main__':
    world = World()
#    world.load_map_from_file('maps/world-non-classic.txt')
    world.load_map_from_file('maps/world-ghostbusters.txt')
    world.wait_after_each_turn = len(sys.argv) > 1

    algo_path = 'lambdaman_algo/smart_algo_implementation.py'
    # ai = LowLevelAI(algo_impl)
    ai = LowLevelAI(algo_path)
    world.set_man_ai(ai)


    # world.set_man_ai(LambdaManAI())
    world.set_ghost_ai(0, RandomGhostAI())
    world.set_ghost_ai(1, RandomGhostAI())
    world.set_ghost_ai(2, RandomGhostAI())
    world.set_ghost_ai(3, RandomGhostAI())

    world.run()
