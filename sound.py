import pygame as pg
#from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.1)
        pacman_sound = pg.mixer.Sound('sounds/pacmaneat.wav')

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def ghost_move(self):
        pg.mixer.music.load('sounds/ghost.wav')
        self.play_bg()

    def scared_ghost(self):
        #self.stop_bg()
        pg.mixer.music.load('sounds/scared_ghost.wav')
        self.play_bg()

    def pacman_death(self):
        self.stop_bg() 
        pg.mixer.music.load('sounds/pacmandeath.wav')
        self.play_bg()
        time.sleep(1.0)

    def pacmaneat(self):
        pg.mixer.music.load('sounds/pacmaneat.wav')
        self.play_bg()

    # def shoot_laser(self, type): 
    #     pg.mixer.Sound.play(self.sounds['alienlaser' if type == LaserType.ALIEN else 'photontorpedo'])
    def gameover(self): 
        self.stop_bg() 
        pg.mixer.music.load('sounds/gameover.wav')
        self.play_bg()
        time.sleep(2.8)
