
import random
import sys
import copy
import os

# directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def next_yx(move, y, x):
    if move == UP: return (y - 1, x)
    if move == RIGHT: return (y, x + 1)
    if move == DOWN: return (y + 1, x)
    if move == LEFT: return (y, x - 1)
    return (y, x)


# cells
GHOST = '='
LAMBDA_MAN = '\\'
EMPTY_CELL = ' '
WALL = '#'
PILL = '.'
POWER_PILL = 'o'
FRUIT = '%'

ticks = {0: [130, 195], 1: [132, 198], 2: [134, 201], 3: [136, 204]}
fruit_cost = {1: 100, 2: 300, 3: 500, 4: 500, 5: 700, 6: 700, 7: 1000, 8: 1000, 9: 2000, 10: 2000, 11: 3000, 12: 3000}

class Creature:
    def __init__(self, y, x, tick_step, tick_step_alt):
        self.y = y
        self.x = x
        self.orig_x = x
        self.orig_y = y
        self.direction = DOWN
        self.next_move = DOWN
        self.ai = None
        self.next_tick = tick_step
        self.tick_step = tick_step
        self.tick_step_alt = tick_step_alt # Not used for man

    def kill(self):
        self.x = self.orig_x
        self.y = self.orig_y
        self.direction = DOWN

    def is_move_legal(self, move):
        return move >= 0 and move < 4

class Man(Creature):
    def __init__(self, y, x, tick_step, tick_step_alt):
        Creature.__init__(self, y, x, tick_step, tick_step_alt)
        self.lives = 3
        self.name = 'man'

    def should_always_move(self):
        return False

class Ghost(Creature):
    def __init__(self, y, x, tick_step, tick_step_alt):
        Creature.__init__(self, y, x, tick_step, tick_step_alt)
        self.name = 'ghost'
        self.visible = True

    def kill(self, visible=False):
        Creature.kill(self)
        self.visible = visible

    def is_move_legal(self, move):
        return Creature.is_move_legal(self, move) and (self.direction == move or (self.direction - move) % 2 != 0)

    def should_always_move(self):
        return True

def print_data(data):
    for s in data:
        print ''.join(s)

class World:
    def __init__(self):
        self.tick = 0
        self.ghosts = []
        self.man = None
        self.pills_num = 0
        self.score = 0
        self.map_level = 1
        self.alt_mode = False
        self.alt_mode_left = 0;
        self.moved_this_tick = False
        self.ghost_cost = 200
        self.fruit_x = 0
        self.fruit_y = 0
        self.the_beginning = True
        self.wait_after_each_turn = False
        self.show_each_turn = True

        self.prev_score = 0
        self.nothing_changed = 0
        self.should_stop = False

    def load_map_from_file(self, file_name):
        self.data = []
        f = open(file_name, 'rt')
        height = 0
        width = 0
        ghost_num = 0
        ghost_type = 0
        for y, s in enumerate(f.readlines()):
            height += 1
            width = len(s)
            ss = s.strip()
            for x, char in enumerate(ss):
                if char == LAMBDA_MAN:
                    self.man = Man(y, x, 127, 127) # 127 is intentional!!!!
                if char == GHOST:
                    ghost  = Ghost(y, x, ticks[ghost_type][0], ticks[ghost_type][1])
                    ghost_type = (ghost_type + 1) % 4
                    ghost.name += str(ghost_num)
                    ghost_num += 1
                    self.ghosts.append(ghost)
                if char == PILL:
                    self.pills_num += 1
                if char == FRUIT:
                    self.fruit_x = x
                    self.fruit_y = y
            ss = ss.replace(GHOST, EMPTY_CELL)
            ss = ss.replace(LAMBDA_MAN, EMPTY_CELL)
            ss = ss.replace(FRUIT, EMPTY_CELL)
            self.data.append(list(ss))

        S = width * height
        if S % 100 == 0:
            self.map_level = S / 100
        else:
            self.map_level = int(S / 100) + 1
        self.eol = 127 * S * 16
        # print self.ghosts

    def reset_world(self):
        for ghost in self.ghosts:
            ghost.kill(True)
        self.man.kill()

    def set_man_ai(self, ai):
        self.man.ai = ai

    def set_ghost_ai(self, index, ai):
        if index < len(self.ghosts):
            self.ghosts[index].ai = ai


    def show(self):
        data_to_show = copy.deepcopy(self.data)
        man = self.man
        data_to_show[man.y][man.x] = LAMBDA_MAN

        for index, ghost in enumerate(self.ghosts):
            # draw ghosts as numbers
            if ghost.visible:
                data_to_show[ghost.y][ghost.x] = str(index)

        print_data(data_to_show)
        print 'Tick: ' + str(self.tick)
        print 'Pills left: ' + str(self.pills_num)
        print 'Score: ' + str(self.score)
        print 'Alt mode: ' + str(self.alt_mode)
        print 'Alt mode left: ' + str(self.alt_mode_left)
        print 'Next man tick ' + str(self.man.next_tick)
        print 'Lives ' + str(self.man.lives)
    
    def run(self):
        if self.show_each_turn:
            os.system('clear')
            self.show()
        while self.alive() and self.any_pills_left():
            self.maybe_dump_debug_info()
    
            self.moved_this_tick = False
            self.update_creatures()
            if self.moved_this_tick or self.the_beginning:
                if self.show_each_turn:
                    os.system('clear')
                    self.show()
                self.get_next_moves()
            self.update_world()
            self.tick += 1

            if self.should_stop:
                print 'STOPPED'
                self.man.lives = 0
            # if self.tick >= self.eol:
            if self.tick >= self.eol:
                print "EOL!!!!"
                self.man.lives = 0
            self.the_beginning = False
        if not self.any_pills_left():
            self.score *= (self.man.lives + 1)
            print 'Victory!'
            return
        else:
            print 'Game Over'

    def get_next_moves(self):
        self.get_creature_move(self.man)
        if self.wait_after_each_turn:
            raw_input()
        for ghost in self.ghosts:
            self.get_creature_move(ghost)

    def get_creature_move(self, creature):
        if creature.next_tick == self.tick or self.the_beginning:
            creature.direction = creature.next_move
            man_data = (self.alt_mode_left, (self.man.x, self.man.y), self.man.direction, self.man.lives, self.score)
            fruit_left = 0
            if self.tick >= 127 * 200 and self.tick < 127 * 280:
                fruit_left = 127 * 280 - self.tick
            if self.tick >= 127 * 400 and self.tick < 127 * 480:
                fruit_left = 127 * 480 - self.tick
            ghosts = []
            for ghost in self.ghosts:
                vitality = 0
                if not ghost.visible:
                    vitality = 2
                elif self.alt_mode:
                    vitality = 1
                ghosts.append((vitality, (ghost.x, ghost.y), ghost.direction))
            # print 'ghosts = ', ghosts
            world_data = (self.data, man_data, ghosts, fruit_left)
            creature.next_move = creature.ai.get_next_move(None, world_data)
            if self.alt_mode:
                creature.next_tick += creature.tick_step_alt
            else:
                creature.next_tick += creature.tick_step
    
    def update_creatures(self):
        self.update_creature(self.man)
        for ghost in self.ghosts:
            self.update_creature(ghost)

    def update_creature(self, creature):
        if creature.next_tick == self.tick:
            self.moved_this_tick = True
            available_moves = self.get_available_moves(creature)
            if len(available_moves) != 0:
                if not self.apply_move(creature) and creature.should_always_move():
                    if len(available_moves) == 1:
                        self.apply_move(creature, available_moves[0], False)
                    elif not self.apply_move(creature, creature.direction):
                        for move in available_moves:
                            if self.apply_move(creature, move):
                                break


    def apply_move(self, creature, move=-1, do_check=True):
        if move == -1:
            next_move = creature.next_move
        else:
            next_move = move
        y0, x0 = creature.y, creature.x
        y, x = next_yx(next_move, y0, x0)
        if self.data[y][x] == WALL or (do_check and not creature.is_move_legal(next_move)):
            return False
        creature.y = y
        creature.x = x
        return True

    def maybe_dump_debug_info(self):
        if self.tick % 10000 == 0:
            if self.prev_score == self.score:
                self.nothing_changed += 1
                if self.nothing_changed >= 5:
                    self.should_stop = True
            else:
                self.nothing_changed = 0
            self.prev_score = self.score
            print 'Tick = {} ({}%) Score = {}, lives = {}'.format(
                self.tick,
                round(100. * self.tick / self.eol, 1),
                self.score, 
                self.man.lives)

    def get_available_moves(self, creature):
        res = []
        for i in range(0, 4):
            y0, x0 = creature.y, creature.x
            y, x = next_yx(i, y0, x0)
            if self.data[y][x] != WALL:
                res.append(i)
        return res

    def update_world(self):
        if self.alt_mode:
            self.alt_mode_left -= 1
            if self.alt_mode_left == 0:
                self.alt_mode = False
                for ghost in self.ghosts:
                    ghost.visible = True

        if self.tick == 127 * 200 or self.tick == 127 * 400:
            self.data[self.fruit_y][self.fruit_x] = FRUIT
        if self.tick == 127 * 280 or self.tick == 127 * 480:
            self.data[self.fruit_y][self.fruit_x] = EMPTY_CELL

        if self.data[self.man.y][self.man.x] == POWER_PILL:
            self.alt_mode = True
            for ghost in self.ghosts:
                if ghost.direction == DOWN:
                    ghost.direction = UP
                    ghost.next_move = UP
                if ghost.direction == UP:
                    ghost.direction = DOWN
                    ghost.next_move = DOWN
                if ghost.direction == LEFT:
                    ghost.direction = RIGHT
                    ghost.next_move = RIGHT
                if ghost.direction == RIGHT:
                    ghost.direction = LEFT
                    ghost.next_move = LEFT
            self.alt_mode_left = 127 * 20
            self.score += 50
            self.man.next_tick += 10

        if self.data[self.man.y][self.man.x] == PILL:
            self.pills_num -= 1
            self.score += 10
            self.man.next_tick += 10
        if self.data[self.man.y][self.man.x] == FRUIT:
            if self.map_level <= 12:
                self.score += fruit_cost[self.map_level]
            else:
                self.score += 5000
            self.man.next_tick += 10
        self.data[self.man.y][self.man.x] = EMPTY_CELL

        for ghost in self.ghosts:
            if ghost.visible and ghost.x == self.man.x and ghost.y == self.man.y:
                if self.alt_mode:
                    self.score += self.ghost_cost
                    if self.ghost_cost != 1600:
                        self.ghost_cost *= 2
                    ghost.kill()
                else:
                    self.man.lives -= 1
                    self.reset_world()
                    break

    def any_pills_left(self):
        return self.pills_num > 0

    def alive(self):
        return self.man.lives > 0

class AI:
    # virtual
    def get_next_move(self, ghosts, world):
        pass


class RandomGhostAI(AI):
    def get_next_move(self, ghosts, world):
        return random.randint(0, 3)


class KeyboardAI(AI):
    def get_next_move(self, ghosts_code, world):
        while True:
            print "where should I move?"
            key = raw_input()
            if len(key) > 0:
                key = key[0]
                if key == 'w': return UP
                if key == 'a': return LEFT
                if key == 's': return DOWN
                if key == 'd': return RIGHT



def main():
    world = World()
    world.load_map_from_file('maps/world-classic.txt')

    world.set_man_ai(KeyboardAI())
    world.set_ghost_ai(0, RandomGhostAI())
    world.set_ghost_ai(1, RandomGhostAI())
    world.set_ghost_ai(2, RandomGhostAI())
    world.set_ghost_ai(3, RandomGhostAI())

    world.run()


if __name__ == '__main__':
    main()
