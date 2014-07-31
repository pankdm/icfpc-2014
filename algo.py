from emulator import *
from algo_implementation import *
from world_converter import *

class LambdaManAI(AI): 
    def get_next_move(self, ai_state, world_state):
        return main(ai_state, convert_world(world_state))[1]

if __name__ == '__main__':
    world = World()
    world.load_map_from_file('maps/world-classic.txt')
    world.wait_after_each_turn = len(sys.argv) > 1

    world.set_man_ai(LambdaManAI())
    world.set_ghost_ai(0, RandomGhostAI())
    world.set_ghost_ai(1, RandomGhostAI())
    world.set_ghost_ai(2, RandomGhostAI())
    world.set_ghost_ai(3, RandomGhostAI())

    world.run()
