# magic spells to include files from outer dir
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from emulator import *
# from lambdaman_algo.smart_algo_implementation import *
from world_converter import *
from chase_ghost_ai import ChaseGhostAI
from lambda_ai import *

def run_on_the_map(map_name):
    print
    print 'Running on', map_name
    world = World()
    # world.load_map_from_file('maps/world-non-classic.txt')
    world.load_map_from_file(map_name)
    world.wait_after_each_turn = len(sys.argv) > 1
    world.show_each_turn = False

    algo_impl = 'lambdaman_algo/smart_algo_implementation.py'
    # ai = LowLevelAI(algo_impl)
    ai = LambdaManAI()

    world.set_man_ai(ai)
    for i in xrange(len(world.ghosts)):
        world.set_ghost_ai(i, ChaseGhostAI(i))
        # world.set_ghost_ai(i, RandomGhostAI())

    world.run()
    print 'Score = {}, lives = {}'.format(
        world.score, world.man.lives)
    # world.show()    

if __name__ == '__main__':
    DIR = 'maps_tournament/'
    run_on_the_map(DIR + 'world-classic.txt')
    # run_on_the_map(DIR + 'world-1.txt')
    # run_on_the_map(DIR + 'world-2.txt')
    # run_on_the_map(DIR + 'ghostbusters.txt')
    # run_on_the_map(DIR + 'ours4.txt')
    # run_on_the_map(DIR + 'ours5.txt')
    # run_on_the_map(DIR + 'map100.txt')
