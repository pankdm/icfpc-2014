
from emulator import *
from world_converter import *

class ChaseGhostAI(AI):
    def __init__(self, index):
        self.index = index

    def get_next_move(self, ghosts, world):
        # print self.index, 'was asked to move'

        # for f in world[0]:
        #     print ''.join(f)
        field = world[0]
        # for f in field:
        #     print ''.join(f)

        ghosts = world[2]
        # print 'ghosts = ', ghosts
        i_am_xy = ghosts[self.index][1]
        man_xy = world[1][1]
        # print 'I am at', i_am_xy
        # print 'Man at', man_xy

        # x, y
        directions = {
            0: (0, -1),
            1: (1, 0),
            2: (0, 1),
            3: (-1, 0)
        }

        x0, y0 = i_am_xy
        mx, my = man_xy

        best = 100000
        direction = 0
        for d, dxy in directions.items():
            dx = dxy[0]
            dy = dxy[1]
            x = x0 + dx
            y = y0 + dy
            # print 'checking', (x, y)
            # print len(field)
            # print len(field[y])
            if field[y][x] != '#':
                diff = abs(mx - x) + abs(my - y)
                if diff < best:
                    best = diff
                    direction = d

        # print 'will go to ', d
        # raw_input('Press Enter')
        return d


