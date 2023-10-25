import pygame as pg 
# import pygame.font

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (200, 200, 200)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None

        self.prep_score()
        self.prep_high_score()

    def increment_score(self, points): 
        self.score += points

        file = open("highscore.txt", "r")
        
        self.high_score_read = file.read()
        self.high_score = int(self.high_score_read.strip())
        file.close()
        if self.score > self.high_score:
            self.high_score = self.score
            file = open("highscore.txt", "w+")
            file.write(str(self.high_score))
            file.close()

        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, (0, 0, 0))

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        self.high_score_display = self.font.render("HIGHSCORE:", True, self.text_color, None)
        file = open("highscore.txt", "r")
        self.high_score_number = self.font.render(file.read(), True, self.text_color, None)
        file.close()

    def reset(self): 
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_display, (0, 25))#(self.settings.screen_w-775, self.settings.screen_h-780))
        self.screen.blit(self.high_score_number, (250, 25))