import pygame as pg

class Node:
    def __init__(self, row, col, box_type, game):
        self.settings = game.settings
        self.size = self.settings.box_size
        self.row = row
        self.col = col
        self.x = col * self.size
        self.y = row * self.size + 105
        self.pos_x = col * self.size + self.size / 2
        self.pos_y = row * self.size + 132 - self.size / 2
        self.screen = game.screen
        # 0 = wall, 1 = node (pill), 2 = spawn, 3 = node (no pill)
        self.box_type = box_type
        # teleport nodes are paired with numbers other than 0, 1, 2, or 3
        self.teleport_to_node = box_type if box_type not in [0, 1, 2, 3] else None
        self.has_pill = bool(box_type == 1 or box_type == 11)
        self.has_power_pill = bool(box_type == 11)
        self.pill = pg.Rect(self.pos_x, self.pos_y, 5, 5)
        self.power_pill = pg.Rect(self.pos_x - 3, self.pos_y - 3, 10, 10)

    def eat_pill(self):
        self.pill = False

    def draw(self):
        if self.has_pill:
            if self.has_power_pill:
                pg.draw.rect(self.screen, (255, 255, 0), self.power_pill)
            else:
                pg.draw.rect(self.screen, (255, 255, 0), self.pill)

    def update(self):
        self.draw()
