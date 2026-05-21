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
        self.current_time = None
        self.point_start = None
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
            game.current_state = "point_start"
            self.point_start = self.current_time
        elif self.current_state == "point_start":
            player.draw()
            ai.draw()
            score.draw()
            if pygame.time.get_ticks() - self.point_start >= 0000 and pygame.time.get_ticks() - self.point_start < 1000:
                text_surf = font.render("3", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
                window.blit(text_surf, text_rect)
                # play beep
            elif pygame.time.get_ticks() - self.point_start >= 1000 and pygame.time.get_ticks() - self.point_start < 2000:
                text_surf = font.render("2", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
                window.blit(text_surf, text_rect)
                # play beep
            elif pygame.time.get_ticks() - self.point_start >= 2000 and pygame.time.get_ticks() - self.point_start < 3000:
                text_surf = font.render("1", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
                window.blit(text_surf, text_rect)
                # play beep
            elif pygame.time.get_ticks() - self.point_start >= 3000 and pygame.time.get_ticks() - self.point_start < 4000:
                text_surf = font.render("GO!", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
                window.blit(text_surf, text_rect)
                # play beeeeeeeeeeeep
            else:
                game.current_state = "in_play"
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

class ScoreTracker(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        pass

    def draw(self):
        pass

# -------------------------------------------------------------
# functions
# -------------------------------------------------------------

def draw_splash():
    # the background image
    scaled_splash = pygame.transform.scale(splash_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_splash, (0, 0))
    # start game instructions
    prompt_surf = font.render("Press any key", True, (240, 240, 240))
    prompt_rect = prompt_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    show_prompt = (pygame.time.get_ticks() // 500) % 2 == 0 # flips between True and False every half second
    if show_prompt:
        window.blit(prompt_surf, prompt_rect)

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
    if event.type == pygame.KEYDOWN and game.current_state == "splash": # if any key is pressed from the splsh screen
        game.state()
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT: # if q is pressed, or the window is 'x'ed out
        game.quit()

# -------------------------------------------------------------
# setup
# -------------------------------------------------------------

pygame.init()

# window
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync = 1)
pygame.display.set_caption("P0N6")

# game running
game = GameState()
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
# pre-loop class initialisations
# -------------------------------------------------------------

player = PlayerPaddle()
ai = AiPaddle()
score = ScoreTracker()
ball = Ball()

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while game.app_running:
    dt = clock.tick(60) / 1000
    game.current_time = pygame.time.get_ticks()

    for event in pygame.event.get(): # if input events happen (keyboard, mouse etc)
        input_handling(event)

    if game.current_state == "splash":
        draw_splash()
    if game.current_state == "point_start":
        game.state()
    elif game.current_state == "match_end":
        draw_match_end()
    else:
        draw_game(dt)

    pygame.display.update()

pygame.quit()