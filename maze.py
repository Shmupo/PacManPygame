import pygame as pg
from node import Node

# create all the maps here

class Maze():
    def __init__(self, game, map_):
        self.settings = game.settings
        self.nodes = []
        self.map = map_
        self.adj_list = None
        self.wall = pg.Rect(0, 104, 28, 28)
        self.game = game
        self.screen = self.game.screen
        self.walls_image = None
        self.adj_list = {}
        self.image = None
        self.start_node = None
        self.ghost_node = None

    # adds adjacent nodes to node in adj_list
    # dictionary key and value are tuples
    def add_adj_node(self, row, col, neighbor):
        if (row, col) in self.adj_list:
            self.adj_list[(row, col)].append(neighbor)
        else:
            self.adj_list[(row,col)] = [neighbor]

    # generate the adjacency lists for each node
    def generate_adj_list(self, row, col):
        for node in self.nodes:
            if (node.col + 1 == col or node.col -1 == col) and node.row == row:
                self.add_adj_node(row, col, node)
            elif (node.row + 1 == row or node.row - 1 == row) and node.col == col:
                self.add_adj_node(row, col, node)

    # creates a node at the coordinates and passes adjacent nodes to it
    def generate_node(self, row, col, node_type):
        node = Node(row, col, node_type, self.game)
        if node_type == 2 : self.start_node = node
        if node_type == 10 : self.ghost_node = node
        self.nodes.append(node)

    # draws the walls of the map once and generated nodes
    # only needs to be called once at the start
    # once generated, an image of the map is stored into self.image
    def generate_map(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                self.wall.x = self.settings.box_size * col
                # draw walls
                if self.map[row][col] == 0: pg.draw.rect(self.screen, (100, 100, 100), self.wall)
                # create nodes and update adj_list
                else: 
                    self.generate_node(row, col, self.map[row][col])
                # create teleport
            self.wall.y = self.settings.box_size * row + 132
        self.wall.y = 104
        self.wall.x = 0

        self.image = self.screen.copy()

        for node in self.nodes:
            self.generate_adj_list(node.row, node.col)

    def update(self):
        self.draw()
        for node in self.nodes:
            node.update()

    # draw only the nodes
    def draw(self):
        if self.image:
            self.screen.blit(self.image, (0, 0))