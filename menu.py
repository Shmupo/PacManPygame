import pygame as pg
import pygame.font as pf
import time
from timer import Timer

title = pg.transform.rotozoom(pg.image.load(f'images/NewTitle.png'), 0, .5)
play_button = pg.transform.rotozoom(pg.image.load(f'images/play_button.png'), 0, .5)

class Menu:
    blue_ghost = [pg.image.load('images/bgr3.png'), pg.image.load('images/bgr4.png')]
    orange_ghost = [pg.image.load('images/ogr3.png'), pg.image.load('images/ogr4.png')]
    pink_ghost = [pg.image.load('images/pgr3.png'), pg.image.load('images/pgr4.png')]
    red_ghost = [pg.image.load('images/rgr3.png'), pg.image.load('images/rgr4.png')]
    pacman = [pg.image.load('images/pmr0.png'), pg.image.load('images/pmr1.png')]
    
    def __init__(self, game, settings, msg):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect(center = (settings.screen_w-200, settings.screen_h - 50))
        self.settings = settings

        self.reset_stats()
        self.game_active = False

        self.bg_color = (0, 0, 0)

        #self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.gamefont = pf.SysFont(None, 48, False, False)
        self.titlefont = pf.SysFont(None, 64, True, False)

        self.rect = pg.Rect(0, 0, self.settings.screen_w, self.settings.screen_h)
        self.rect.center = self.screen_rect.center

        self.image = pg.image.load('images/pacmantitlepage.png')
        self.timer_blue_ghost = Timer(self.blue_ghost)
        self.timer_orange_ghost = Timer(self.orange_ghost)
        self.timer_pink_ghost = Timer(self.pink_ghost)
        self.timer_red_ghost = Timer(self.red_ghost)
        self.timer_pacman = Timer(self.pacman)
        self.x, self.y = 0, 480
        self.rect = self.image.get_rect()

        self.surface = pg.display.set_mode((self.settings.screen_w-10, self.settings.screen_h-10))


        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.gamefont.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

        file = open("highscore.txt", "r")
        self.highscorevalue = self.gamefont.render(file.read(), True, self.text_color, None)
        file.close()

        self.highscoredisplay = self.gamefont.render("HIGHSCORE:", True, self.text_color, None)

    def reset_stats(self):
        self.lives_left = self.settings.pacman_lives
        self.score = 0

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(title, (0, 0))

        #surface = pg.display.set_mode((self.settings.screen_w-10, self.settings.screen_h-10))
        #pg.draw.rect(self.surface, (0, 0, 0), pg.Rect(0, 480, self.settings.screen_w, 50))

        self.screen.blit(play_button, (430, 780))
        #self.screen.blit(self.highscoredisplay, (self.settings.screen_w/5, self.settings.screen_h-300))
        self.screen.blit(self.highscorevalue, (300, 90))
        
        
        self.screen.blit(self.timer_blue_ghost.imagerect(), (self.x+10, self.y))
        self.screen.blit(self.timer_orange_ghost.imagerect(), (self.x+110, self.y))
        self.screen.blit(self.timer_pink_ghost.imagerect(), (self.x+210, self.y))
        self.screen.blit(self.timer_red_ghost.imagerect() , (self.x+310, self.y))
        self.screen.blit(self.timer_pacman.imagerect(), (self.x+410, self.y))
            
        self.x += 10
        time.sleep(0.1)
            
            
            
            

