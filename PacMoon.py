# Andrew Doan

# Pac Man Project

import pygame as pg
from maze import Maze
from ghosts import *
from settings import Settings
from player import Player
import game_functions as gf
from menu import Menu
from scoreboard import Scoreboard
from sound import Sound
import sys

import maps

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        
        size = self.settings.screen_w, self.settings.screen_h
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption('PacMoon')
        self.sound = Sound(bg_music="sounds/pacmantheme.wav")

        self.map_start = None
        self.scoreboard = Scoreboard(game=self)
        self.maze = Maze(self, maps.map0)
        self.maze.generate_map()
        self.player = Player(self)
        self.pink_ghost = Pink(self)
        self.blue_ghost = Blue(self)
        self.orange_ghost = Orange(self)
        self.red_ghost = Red(self)
        self.menu = Menu(self, self.settings, "Play")
        

    def reset(self):
        print("Resetting Game")
        #self.maze = Maze(self, maps.map0)
        self.maze.generate_map()
        self.player.reset(game=self)
        self.scoreboard.reset()

    def game_over(self):
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:
            gf.check_events(self, self.player)
            if not self.menu.game_active:
                #self.sound.play_bg()
                self.menu.draw()
            else:
                #self.sound.stop_bg()
                self.maze.update()
                self.pink_ghost.update()
                self.blue_ghost.update()
                self.orange_ghost.update()
                self.red_ghost.update()
                self.player.update()
                self.scoreboard.update()
            pg.display.flip()

def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()


