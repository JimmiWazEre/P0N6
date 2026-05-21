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
from random import uniform, choice
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

    def state(self, dt, direction):
        if self.current_state == "splash":
            self.point_start = self.current_time
            self.current_state = "point_start"
        elif self.current_state == "point_start":
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
                # launch the ball
                game.current_state = "in_play"
        elif self.current_state == "in_play":
            player.update(dt, direction)
            ai.update(dt)
            score.update(dt)
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
    def __init__(self, *groups):
        super().__init__(*groups)
        self.speed = 150

    def update(self, dt, direction):
        self.rect.center += self.speed * direction * dt

class AiPaddle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        pass

    def update(self, dt):
        self.rect.center += self.velocity * dt

class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((15, 15)) # create a blank 15x15 canvas
        self.image.fill("white") # paint it white - this is the visible ball
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) # get a rect from the surface, centered on screen - this is the ball's position
        self.speed = None
        self.velocity = None

    def launch(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.speed = 100
        self.velocity = pygame.Vector2(choice([-1, 1]), uniform(-1.5, 1.5)) * self.speed # random left or right, slight random vertical angle

    def update(self, dt):
        self.rect.center += self.velocity * dt # move the ball each frame - pygame redraws self.image at self.rect.center automatically via the sprite group

class ScoreTracker(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        pass

    def update(self, dt):
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

def input_handling(event, dt):
    keys = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN and game.current_state == "splash":
        game.state(dt)
    elif event.key == pygame.K_q or event.type == pygame.QUIT:
        game.quit()
    if event.type == pygame.KEYDOWN and event.key == pygame.Y_UP:
        direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        game.state(dt, direction)

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

player = PlayerPaddle(game.all_sprites, game.paddle_sprites)
ai = AiPaddle(game.all_sprites, game.paddle_sprites)
score = ScoreTracker(game.all_sprites)
ball = Ball(game.all_sprites, game.ball_sprites)

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while game.app_running:
    dt = clock.tick(60) / 1000
    game.current_time = pygame.time.get_ticks()

    for event in pygame.event.get(): # if input events happen (keyboard, mouse etc)
        input_handling(event, dt)

    if game.current_state == "splash":
        draw_splash()
    elif game.current_state == "point_start":
        game.state(dt)
    elif game.current_state == "in_play":
        game.state(dt)
    elif game.current_state == "match_end":
        draw_match_end()
    else:
        draw_game(dt)

    pygame.display.update()

pygame.quit()