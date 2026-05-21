"""

=============================================================
P0N6
=============================================================

-------------------------------------------------------------
CONTROLS
-------------------------------------------------------------
Arrow keys      Move paddle
Space           Launch ball
ESC             Pause / unpause
R               Restart (game over screen)


-------------------------------------------------------------
REFERENCES
-------------------------------------------------------------
pygame-ce docs      https://pyga.me/docs/

"""

import pygame
from os.path import dirname, abspath, join
from os.path import expanduser
BASE_DIR = dirname(abspath(__file__))

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class GameState():
    def __init__(self):
        self.app_running = True
        self.current_state = "splash"
        self.current_time = 0
        self.score = {"player": 0, "ai": 0}
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()

    def reset(self):
        self.app_running = True
        self.current_state = "point_start"
        self.current_time = 0
        self.score = {"player": 0, "ai": 0}
        self.all_sprites.empty()
        self.paddle_sprites.empty()
        self.ball_sprites.empty()

    def state(self):
        if self.current_state == "splash":
            #consequence
        elif self.current_state == "point_start":
            #consequence
        elif self.current_state == "in_play":
            #consequence
        elif self.current_state == "point_scored":
            #consequence
        elif self.current_state == "paused":
            #consequence
        elif self.current_state == "match_end":
            #consequence
    
    def quit(self):
        self.app_running = False

    def toggle_pause(self, event):
        pass

    def start_game(self, event):
        if self.current_state == "splash":
            self.reset()

# sprite classes

class PlayerPaddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        pass

    def draw(self):
        pass

    def input(self, event):
        pass

class AiPaddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        pass

    def draw(self):
        pass

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        pass

    def draw(self):
        pass

class Score(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        pass

    def draw(self):
        pass

# -------------------------------------------------------------
# functions
# -------------------------------------------------------------

def draw_splash():
    pass

def draw_background():
    pass

def draw_match_end():
    pass

def draw_game(dt):
    pass

def collisions():
    pass

def update_game(dt):
    pass

def input_handling(event):
    if event.type == pygame.KEYDOWN and state.current_state == "splash":
        state.current_state = "point_start"
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        state.quit()

# -------------------------------------------------------------
# setup
# -------------------------------------------------------------

pygame.init()

# window
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
pygame.display.set_caption("P0N6")

# game running
state = GameState()
clock = pygame.time.Clock()

# -------------------------------------------------------------
# assets
# -------------------------------------------------------------

# images
splash_surf = pygame.image.load(join(BASE_DIR, "images", "splash.png")).convert()

# fonts
font = pygame.font.Font(join(BASE_DIR, "PressStart2P-Regular.ttf"), 20)

# sounds

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while state.app_running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        input_handling(event)

    if state.current_state == "splash":
        draw_splash()
    elif state.current_state == "match_end":
        draw_match_end()
    else:
        draw_game(dt)

    pygame.display.update()

pygame.quit()