import pygame as pg
import sys

# checking player inputs
def check_events(self, player):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN: 
            key = event.key
            if key == pg.K_UP: player.direction = 1
            elif key == pg.K_RIGHT: player.direction = 2
            elif key == pg.K_DOWN: player.direction = 3
            elif key == pg.K_LEFT: player.direction = 4
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            check_play(self, mouse_pos)
    
def check_play(self, mouse_pos):
    button_clicked = pg.Rect(430, 780, 250, 100).collidepoint(mouse_pos)
    if button_clicked and not self.menu.game_active:        
        self.menu.reset_stats()
        self.menu.game_active = True

        self.pink_ghost.reset()
        self.blue_ghost.reset()
        self.orange_ghost.reset()
        self.red_ghost.reset()
        
        self.player.reset(game=self)

        pg.mouse.set_visible(False)