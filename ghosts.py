import pygame as pg
import time
from timer import Timer


# base ghost class
class Ghost:

        #images of ghost when pill is eaten
        pill_ghost = [pg.image.load(f'images/dying0.png'), pg.image.load(f'images/dying1.png'),
                      pg.image.load(f'images/dying2.png'), pg.image.load(f'images/dying3.png')]

        dead_up = [pg.image.load(f'images/deadup.png')]
        dead_right = [pg.image.load(f'images/deadright.png')]
        dead_down = [pg.image.load(f'images/deaddown.png')]
        dead_left = [pg.image.load(f'images/deadleft.png')]
    
        def __init__(self, game, up_images, right_images, down_images, left_images):
            self.game = game
            self.settings = game.settings
            self.screen = game.screen
            self.size = self.settings.box_size
            self.image = pg.transform.scale(pg.image.load(f'images/pgu3.png'), (self.size, self.size))
            self.rect = self.image.get_rect()
            self.nodes = game.maze.nodes
            self.spawn_node = game.maze.ghost_node
            self.node = game.maze.ghost_node
            self.player = game.player
            self.timer_up = Timer(self.up_images)
            self.timer_right = Timer(self.right_images)
            self.timer_down = Timer(self.down_images)
            self.timer_left = Timer(self.left_images)
            # this is the next adjacent node to move to
            self.to_node = self.node
            self.adj_list = game.maze.adj_list
            self.player_node = game.player.node
            self.pos_x = self.node.x
            self.pos_y = self.node.y
            self.speed = self.settings.ghost_speed
            # True for testing
            # Each define the state the ghost is in
            self.scattering = True
            self.chase = False
            self.running = False
            self.circling = False
            self.direction = 1
            self.moving = False
            self.moves = []
            self.sound = game.sound
            self.respawning = False
            self.scoreboard = game.scoreboard

            self.dying = False
            self.power_up = False
            self.start = time.time()

            self.wait_time = time.time()

            # scaling images
            for x in range(len(self.up_images)):
                self.up_images[x] = pg.transform.scale(self.up_images[x], (self.settings.box_size, self.settings.box_size))
                self.right_images[x] = pg.transform.scale(self.right_images[x], (self.settings.box_size, self.settings.box_size))
                self.down_images[x] = pg.transform.scale(self.down_images[x], (self.settings.box_size, self.settings.box_size))
                self.left_images[x] = pg.transform.scale(self.left_images[x], (self.settings.box_size, self.settings.box_size))
            
            for x in range(len(self.dead_up)):
                self.dead_up[x] = pg.transform.scale(self.dead_up[x], (self.settings.box_size, self.settings.box_size))
                self.dead_right[x] = pg.transform.scale(self.dead_right[x], (self.settings.box_size, self.settings.box_size))
                self.dead_down[x] = pg.transform.scale(self.dead_down[x], (self.settings.box_size, self.settings.box_size))
                self.dead_left[x] = pg.transform.scale(self.dead_left[x], (self.settings.box_size, self.settings.box_size))

            for x in range(len(self.pill_ghost)):
                self.pill_ghost[x] = pg.transform.scale(self.pill_ghost[x], (self.settings.box_size, self.settings.box_size))
            
            # keep track of time in seconds
            self.init_time = time.time()
            self.timer = self.image
            self.timer_pill_ghost = Timer(self.pill_ghost)

            self.timer_dead_up = Timer(self.dead_up)
            self.timer_dead_right = Timer(self.dead_right)
            self.timer_dead_down = Timer(self.dead_down)
            self.timer_dead_left = Timer(self.dead_left)

            self.corner_node = None

        # returns the node closest to the direction of the target node
        # used for choosing which path to take in an intersection
        def best_node(self, node):
            self.check_moves()
            if len(self.moves) > 2:
                best_node = None
                best_distance = float("inf")
                if not self.running:
                    for n in self.adj_list[(self.node.row, self.node.col)]:
                        distance = (node.x - n.x) ** 2 + (node.y - n.y) ** 2
                        if distance < best_distance: 
                            best_distance = distance
                            best_node = n
                elif self.running:
                    best_distance = 0
                    for n in self.adj_list[(self.node.row, self.node.col)]:
                        distance = (node.x - n.x) ** 2 + (node.y - n.y) ** 2
                        if distance > best_distance: 
                            best_distance = distance
                            best_node = n

                if best_node.row == self.node.row - 1 and self.direction != 3: self.direction = 1
                if best_node.col == self.node.col + 1 and self.direction != 4: self.direction = 2
                if best_node.row == self.node.row + 1 and self.direction != 1: self.direction = 3
                if best_node.col == self.node.col - 1 and self.direction != 2: self.direction = 4

                if self.direction not in self.moves:
                    self.direction = self.moves[0]
                return self.node_in_direction(self.direction)

            elif self.direction in self.moves:
                return self.node_in_direction(self.direction)
            else:
                for m in self.moves:
                    if self.direction == m: 
                        self.direction = m
                        return self.node_in_direction(m)
                    else: 
                        self.direction = m
                        return self.node_in_direction(m)

        # changes which images to use when changing direction
        def face_direction(self):
            if self.moving and not self.respawning and not self.power_up and not self.dying:
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
            elif self.moving and not self.respawning and self.power_up and not self.dying:
                self.sound.scared_ghost()
                self.timer = self.timer_pill_ghost
                self.image = self.timer.imagerect()
            elif self.moving and not self.respawning and self.dying:
                if self.direction == 1:
                    self.timer = self.timer_dead_up
                elif self.direction == 2:
                    self.timer = self.timer_dead_right
                elif self.direction == 3:
                    self.timer = self.timer_dead_down
                elif self.direction == 4:
                    self.timer = self.timer_dead_left 
                if self.timer != None:
                    self.timer.wait_for_command = False
                    self.image = self.timer.imagerect()


        # used by search algorithms to move to an adjacent node
        # moving set to false once the ghost is on the target node
        def move_to_adjacent(self, node):
            row = self.node.row
            col = self.node.col

            if self.pos_x != node.x or self.pos_y != node.y: self.moving = True
            else:
                self.node = node
                self.moving = False

            # if moving, move towards target node
            if self.moving:
                self.sound.ghost_move()
                if(row == node.row):
                    # right
                    if self.direction == 2: self.pos_x += self.speed
                    # left
                    elif self.direction == 4: self.pos_x -= self.speed
                elif(col == node.col):
                    # down
                    if self.direction == 3: self.pos_y += self.speed
                    # up
                    elif self.direction == 1: self.pos_y -= self.speed
        
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

        # returns the node in the current facing direction
        def node_in_direction(self, direction):
            for node in self.adj_list[(self.node.row, self.node.col)]:
                if direction == 1: 
                    if node.row == self.node.row - 1: return node
                elif direction == 2:
                    if node.col == self.node.col + 1: return node
                elif direction == 3:
                    if node.row == self.node.row + 1: return node
                elif direction == 4:
                    if node.col == self.node.col - 1: return node

        # once at the ghosts corner, start going in circles
        def circle_path(self):
            self.check_moves()
            if self.direction == 1 and 4 in self.moves: self.direction = 4
            elif self.direction == 2 and 1 in self.moves: self.direction = 1
            elif self.direction == 3 and 2 in self.moves: self.direction = 2
            elif self.direction == 4 and 3 in self.moves: self.direction = 3

            return self.node_in_direction(self.direction)

        # changes the behaviour of the ghost according to a timer
        # 7 seconds for scatter
        # 20 seconds for chase
        def set_mode(self):
            if self.scattering:
                if time.time() - self.init_time > 5:
                    self.init_time = time.time()
                    self.chase = True
                    self.scattering = False
                    self.pathing = False
            elif self.chase:
                if time.time() - self.init_time > 5:
                    self.init_time = time.time()
                    self.chase = False
                    self.scattering = True
                    self.circling = False
                    self.pathing = False

        # return to spawn node when killed
        def respawn(self):
            pass

        def reset(self):
            self.node = self.spawn_node
            self.pos_x = self.spawn_node.x
            self.pos_y = self.spawn_node.y
            self.moving = False
            self.init_time = time.time()
            self.direction = 1
            self.chase = False
            self.scattering = True
            self.scared = False
            self.circling = False
        
        def hit(self):
            if not self.dying:
                print("Ghost Hit")
                self.scoreboard.increment_score(1000)
                self.dying = True
                self.respawing = True

        def check_collision(self):
            rect = pg.Rect(self.pos_x, self.pos_y, self.settings.box_size, self.settings.box_size)
            collisions = rect.colliderect(self.player.rect)#pg.Rect.colliderect(self.player.rect, (self.player.pos_x, self.player.pos_y), self.rect, (self.pos_x, self.pos_y))
            if collisions and self.power_up:
                self.hit()
            elif collisions and not self.power_up:
                self.player.hit()

        def player_ate_pill(self):
            if self.player.node.box_type == 11: 
                self.power_up = True
                self.running = True
                self.circling = False
                self.scattering = False
                self.start = time.time()
            if time.time() - self.start > 5 and self.running == True:
                self.power_up = False
                self.running = False
                self.scattering = True
                
        def update(self):
            self.moves = []

            self.set_mode()
            self.player_ate_pill()
            self.check_collision()
            self.face_direction()
            # self.player_ate_pill()

            if self.game.player.dying:
                self.reset()
            
            if self.moving == False:
                # circle-scatter mode
                if self.scattering == True and self.circling == True:
                    self.to_node = self.circle_path()
                # go to corner to start circling
                elif self.scattering == True:
                    if self.node != self.corner_node:
                        self.to_node = self.best_node(self.corner_node)
                    elif self.node == self.corner_node: self.circling = True
                # targeting mode
                elif self.chase == True:
                    if not self.pathing:
                        self.to_node = self.best_node(self.game.player.node)
                # running mode
                if self.running == True:
                    self.to_node = self.best_node(self.player.node)
                if self.dying == True:
                    self.to_node = self.best_node(self.spawn_node)
                    self.running = False
                if self.node == self.spawn_node:
                    self.dying = False
                    self.respawing = False
                    self.scattering = True
                    self.power_up = False
            
            if self.to_node != None: self.move_to_adjacent(self.to_node)
            else: self.moving = False
            self.draw()

        def draw(self):
            self.screen.blit(self.image, (self.pos_x, self.pos_y))

class Pink(Ghost):
    def __init__(self, game):
        self.up_images = [pg.image.load(f'images/pgu3.png'), pg.image.load(f'images/pgu4.png')]
        self.right_images = [pg.image.load(f'images/pgr3.png'), pg.image.load(f'images/pgr4.png')]
        self.down_images = [pg.image.load(f'images/pgd3.png'), pg.image.load(f'images/pgd4.png')]
        self.left_images = [pg.image.load(f'images/pgl3.png'), pg.image.load(f'images/pgl4.png')]

        super().__init__(game, self.up_images, self.right_images, self.down_images, self.left_images)

        # top left
        for node in self.nodes:
                if node.row == 1 and node.col == 6:
                    self.corner_node = node

class Blue(Ghost):
    def __init__(self, game):
        self.up_images = [pg.image.load(f'images/bgu3.png'), pg.image.load(f'images/bgu4.png')]
        self.right_images = [pg.image.load(f'images/bgr3.png'), pg.image.load(f'images/bgr4.png')]
        # need bgd4.png
        self.down_images = [pg.image.load(f'images/bgd4.png'), pg.image.load(f'images/bgd4.png')]
        self.left_images = [pg.image.load(f'images/bgl3.png'), pg.image.load(f'images/bgl4.png')]

        super().__init__(game, self.up_images, self.right_images, self.down_images, self.left_images)
        
        # bottom right
        for node in self.nodes:
                if node.row == 21 and node.col == 20:
                    self.corner_node = node

    def circle_path(self):
        self.check_moves()
        if self.direction == 2 and 3 in self.moves: self.direction = 3
        elif self.direction == 2 and 2 not in self.moves : self.direction = 1
        elif self.direction == 3:
            for m in self.moves:
                self.direction = m
        elif self.direction == 1 and 2 in self.moves: self.direction = 2
        elif self.direction == 4 and 1 in self.moves: self.direction = 1

        return self.node_in_direction(self.direction)

    # blue runs from player when too close to player
    def set_mode(self):
            if self.scattering:
                if time.time() - self.init_time > 5:
                    self.init_time = time.time()
                    self.chase = True
                    self.scattering = False
                    self.pathing = False
            elif self.chase:
                if (abs(self.node.x - self.player.node.x) + abs(self.node.y - self.player.node.y)) < 200 or (time.time() - self.init_time > 5):
                    self.init_time = time.time()
                    self.chase = False
                    self.scattering = True
                    self.circling = False
                    self.pathing = False

    def set_mode(self):
        if self.wait_time - time.time() > 15:
            super().set_mode()

class Orange(Ghost):
    def __init__(self, game):
        self.up_images = [pg.image.load(f'images/ogu3.png'), pg.image.load(f'images/ogu4.png')]
        self.right_images = [pg.image.load(f'images/ogr3.png'), pg.image.load(f'images/ogr4.png')]
        self.down_images = [pg.image.load(f'images/ogd3.png'), pg.image.load(f'images/ogd4.png')]
        self.left_images = [pg.image.load(f'images/ogl3.png'), pg.image.load(f'images/ogl4.png')]

        super().__init__(game, self.up_images, self.right_images, self.down_images, self.left_images)
        
        # bottom left
        for node in self.nodes:
                if node.row == 21 and node.col == 6:
                    self.corner_node = node

    def circle_path(self):
        self.check_moves()
        
        if self.direction == 3 and 4 in self.moves: self.direction = 4
        elif self.direction == 3 and 3 not in self.moves: self.direction = 2
        elif self.direction == 2 and 1 in self.moves: self.direction = 1
        elif self.direction == 1 and 4 in self.moves: self.direction = 4
        elif self.direction == 4 and 3 in self.moves: self.direction = 3
        elif self.direction == 4 and 4 not in self.moves: self.direction = 1

        return self.node_in_direction(self.direction)

    def set_mode(self):
        if self.wait_time - time.time() > 10:
            super().set_mode()

class Red(Ghost):
    def __init__(self, game):
        self.up_images = [pg.image.load(f'images/rgu3.png'), pg.image.load(f'images/rgu4.png')]
        self.right_images = [pg.image.load(f'images/rgr3.png'), pg.image.load(f'images/rgr4.png')]
        self.down_images = [pg.image.load(f'images/rgd3.png'), pg.image.load(f'images/rgd4.png')]
        self.left_images = [pg.image.load(f'images/rgl3.png'), pg.image.load(f'images/rgl4.png')]

        super().__init__(game, self.up_images, self.right_images, self.down_images, self.left_images)

        # top right
        for node in self.nodes:
                if node.row == 1 and node.col == 21:
                    self.corner_node = node

    def circle_path(self):
        self.check_moves()
        
        if self.direction == 2 and 3 in self.moves: self.direction = 3
        elif self.direction == 3 and 4 in self.moves: self.direction = 4
        elif self.direction == 1 and 2 in self.moves: self.direction = 2
        elif self.direction == 4 and 1 in self.moves: self.direction = 1

        return self.node_in_direction(self.direction)