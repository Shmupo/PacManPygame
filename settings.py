# contains many parameters for different options

class Settings:
    def __init__(self):
        # 28 and 36 are the screen dimension ratios
        # 27 is the size of each box
        self.box_size = 27
        self.screen_w = 27 * self.box_size
        self.screen_h = 36 * self.box_size

        self.player_speed = 1
        self.ghost_speed = 1

        self.width = 1200
        self.height = 800

        self.pacman_lives = 3

        self.pill_point = 10
        self.power_pill_point = 50
