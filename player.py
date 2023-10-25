import pygame as pg
from timer import Timer
from menu import Menu
from sound import Sound

class Player:
    up_images = [pg.image.load(f'images/pm0.png'), pg.image.load(f'images/pmu0.png'), pg.image.load(f'images/pmu1.png'), pg.image.load(f'images/pmu0.png')]
    right_images = [pg.image.load(f'images/pm0.png'), pg.image.load(f'images/pmr0.png'), pg.image.load(f'images/pmr1.png'), pg.image.load(f'images/pmr0.png')]
    down_images = [pg.image.load(f'images/pm0.png'), pg.image.load(f'images/pmd0.png'), pg.image.load(f'images/pmd1.png'), pg.image.load(f'images/pmd0.png')]
    left_images = [pg.image.load(f'images/pm0.png'), pg.image.load(f'images/pml0.png'), pg.image.load(f'images/pml1.png'), pg.image.load(f'images/pml0.png')]

    pmdeath = [pg.image.load(f'images/pmdeath0.png'), pg.image.load(f'images/pmdeath1.png'), pg.image.load(f'images/pmdeath2.png'), 
    pg.image.load(f'images/pmdeath3.png'), pg.image.load(f'images/pmdeath4.png'), pg.image.load(f'images/pmdeath5.png'), 
    pg.image.load(f'images/pmdeath6.png'), pg.image.load(f'images/pmdeath7.png'), pg.image.load(f'images/pmdeath8.png'),
    pg.image.load(f'images/pmdeath9.png'), pg.image.load(f'images/pmdeath10.png'), pg.image.load(f'images/pmdeath11.png')]

    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.lives = 3
        self.direction = 0
        self.adj_list = game.maze.adj_list
        self.nodes = game.maze.nodes
        self.node = game.maze.start_node
        self.still_image = pg.transform.scale(pg.image.load(f'images/pm0.png'), (self.settings.box_size, self.settings.box_size))
        self.image = pg.transform.scale(pg.image.load(f'images/pm0.png'), (self.settings.box_size, self.settings.box_size))
        self.rect = self.image.get_rect()
        self.pos_x = self.node.x
        self.pos_y = self.node.y
        self.size = self.settings.box_size
        self.moving = True #0
        self.moves = []
        self.teleported = 0
        self.scoreboard = game.scoreboard
        self.dying = False
        self.menu = Menu(self, self.settings, "Play")
        self.sound = game.sound
        # scale all images to right size
        for x in range(len(self.up_images)):
            self.up_images[x] = pg.transform.scale(self.up_images[x], (self.settings.box_size, self.settings.box_size))
            self.right_images[x] = pg.transform.scale(self.right_images[x], (self.settings.box_size, self.settings.box_size))
            self.down_images[x] = pg.transform.scale(self.down_images[x], (self.settings.box_size, self.settings.box_size))
            self.left_images[x] = pg.transform.scale(self.left_images[x], (self.settings.box_size, self.settings.box_size))

        for x in range(len(self.pmdeath)):
            self.pmdeath[x] = pg.transform.scale(self.pmdeath[x], (self.settings.box_size, self.settings.box_size))

        self.timer_up = Timer(self.up_images)
        self.timer_right = Timer(self.right_images)
        self.timer_down = Timer(self.down_images)
        self.timer_left = Timer(self.left_images)
        self.timer_pmdeath = Timer(self.pmdeath, looponce = True)
        self.timer = None

    # eat the pill of the current node the player is on
    def eat_pill(self):
        if self.node.has_pill == True: 
            self.node.has_pill = False
            if self.node.box_type == 1:
                self.scoreboard.increment_score(self.settings.pill_point)
            elif self.node.box_type == 11:
                # powers up
                self.scoreboard.increment_score(self.settings.power_pill_point)

    def hit(self):
        if not self.dying:
            print("Hit")
            self.dying = True
            self.moving = False
        else:
            self.menu.game_active = False
            pg.mouse.set_visible(True)

    # changes which images to use when changing direction
    def face_direction(self):
        if self.moving and not self.dying:
            if self.direction == 1:
                self.timer = self.timer_up
            elif self.direction == 2:
                self.timer = self.timer_right
            elif self.direction == 3:
                self.timer = self.timer_down
            elif self.direction == 4:
                self.timer = self.timer_left 
            if self.timer != None:
                self.timer.wait_for_command = False
                self.image = self.timer.imagerect()
            else: self.timer = self.still_image
        else:     
            #self.sound.pacman_death()
            self.timer = self.timer_pmdeath
            self.image = self.timer.imagerect()         


    # (row, col) = (y, x)
    def check_moves(self):
        for node in self.adj_list[(self.node.row, self.node.col)]:
            # up
            if(node.row == self.node.row - 1): self.moves.append(1)
            # right
            if(node.col == self.node.col + 1): self.moves.append(2)
            # down
            if(node.row == self.node.row + 1): self.moves.append(3)
            # left
            if(node.col == self.node.col - 1): self.moves.append(4)

    # sets the node to the node the player is on relative to the center of the player
    def set_node(self, row, col):
        self.moves = []
        for n in self.adj_list[(self.node.row, self.node.col)]:
            if n.row == row and n.col == col:
                if n.x == self.pos_x and n.y == self.pos_y:
                        self.node = n

    # keeps pacman on the path
    def stay_on_path(self):
        if self.moving:
            # left or right
            if self.direction == 4 or self.direction == 2:
                self.pos_y = self.node.y       
            # up or down
            elif self.direction == 1 or self.direction == 3:
                self.pos_x = self.node.x

    # checks if current node is a teleport node, which is any number not already used
    # sets flag so that player can only teleport again after leaving the node after teleporting
    def check_teleport(self):
        if not self.teleported:
            if 3 < self.node.box_type < 10:
                to_node = None
                for node in self.nodes: 
                    if(node.box_type == self.node.box_type):
                        if(self.node != node): to_node = node
                self.pos_x = to_node.x
                self.pos_y = to_node.y
                self.node = to_node
                self.teleported = True
        else:
            if self.node.box_type in [1, 2, 3]: self.teleported = False

    # Checks if movement in direction is valid
    def check_adjacent(self):
        if self.direction in self.moves: self.moving = True
        else: self.moving = False

    # 1 is up, 2 is right, 3 is down, 4 is left
    # directions are determined by the check_events function in game_functions.py
    def move(self):
        self.check_adjacent()
        if self.moving and not self.dying:
            self.sound.pacmaneat()
            if self.direction == 1: 
                self.pos_y -= self.settings.player_speed 
                self.set_node(self.node.row - 1, self.node.col)
            elif self.direction == 2: 
                self.pos_x += self.settings.player_speed 
                self.set_node(self.node.row, self.node.col + 1)
            elif self.direction == 3: 
                self.pos_y += self.settings.player_speed 
                self.set_node(self.node.row + 1, self.node.col)
            elif self.direction == 4: 
                self.pos_x -= self.settings.player_speed
                self.set_node(self.node.row, self.node.col - 1)
            self.rect.x = round(self.pos_x)
            self.rect.y = round(self.pos_y)
        if self.dying:
            self.settings.player_speed *= 0

    def dead(self):
        #if self.dying: #self.timer == self.timer_pmdeath:
        self.lives -= 1
        self.sound.pacman_death()
        if self.lives > 0:
            self.game.reset()
        else: 
            self.game.game_over()
        
    def respawn(self):
        pass

    # when the player dies
    def reset(self, game):
        #self.lives -= 1
        self.adj_list = game.maze.adj_list
        self.nodes = game.maze.nodes
        self.node = game.maze.start_node

        self.direction = 0
        #self.still_image = pg.transform.scale(pg.image.load(f'images/pm0.png'), (self.settings.box_size, self.settings.box_size))

        self.timer = None
        self.timer_pmdeath.reset()
        #self.timer = self.still_image
        self.settings.player_speed = 1
        self.menu.game_active = True

        # self.direction = 0
        # self.adj_list = self.maze.adj_list
        # self.nodes = self.maze.nodes
        # self.node = self.maze.start_node
        self.moving = True #0
        self.moves = []
        self.teleported = 0
        self.dying = False


        #self.timer_pmdeath.reset()
        self.pos_x = self.node.x
        self.pos_y = self.node.y

    def update(self):
        if self.timer == self.timer_pmdeath and self.timer.finished == True:
            self.dead()
        self.check_moves()
        self.eat_pill()
        self.move()
        self.check_teleport()
        self.stay_on_path()
        if self.moving:
            self.face_direction()
        self.draw()

    def draw(self):
        #self.face_direction()
        self.screen.blit(self.image, (self.pos_x, self.pos_y))