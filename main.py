"""

=============================================================
P0N6 FL1P!
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
        self.ball = None
        self.cur_score = 0
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.player = None
        self.ai = None
        self.score = ScoreTracker(self.all_sprites)

    def reset(self):
        self.app_running = True
        self.current_state = "point_start"
        self.current_time = 0
        self.cur_score = 0
        self.all_sprites.empty()
        self.paddle_sprites.empty()
        self.ball_sprites.empty()

    def state(self, dt):
        if self.current_state == "splash":
            self.point_start = self.current_time
            self.current_state = "point_start"
            self.score = ScoreTracker(game.all_sprites)
        elif self.current_state == "point_start":
            self.cur_score = 0
            if self.player:
                self.player.kill()
            if self.ai:
                self.ai.kill()
            if pygame.time.get_ticks() - self.point_start >= 0000 and pygame.time.get_ticks() - self.point_start < 1000:
                text_surf = font.render("3", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
                window.blit(text_surf, text_rect)
                one_sound.play()
            elif pygame.time.get_ticks() - self.point_start >= 1000 and pygame.time.get_ticks() - self.point_start < 2000:
                text_surf = font.render("2", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
                window.blit(text_surf, text_rect)
                two_sound.play()
            elif pygame.time.get_ticks() - self.point_start >= 2000 and pygame.time.get_ticks() - self.point_start < 3000:
                text_surf = font.render("1", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
                window.blit(text_surf, text_rect)
                three_sound.play()
            elif pygame.time.get_ticks() - self.point_start >= 3000 and pygame.time.get_ticks() - self.point_start < 4000:
                text_surf = font.render("GO!", True, (240, 240, 240))
                text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
                window.blit(text_surf, text_rect)
                GO_sound.play()
            else:
                self.ball = Ball(game.all_sprites, game.ball_sprites)
                self.ai = AiPaddle(game.all_sprites, game.paddle_sprites)
                self.player = PlayerPaddle(game.all_sprites, game.paddle_sprites)
                self.ball.launch()
                game.current_state = "in_play"
        elif self.current_state == "in_play":
            self.player.update(dt)
            self.ai.update(dt)
            self.score.update(dt)
            self.ball.update(dt)
            collisions()
        # elif self.current_state == "point_scored":
        #     #consequence
        #     pass
        elif self.current_state == "paused":
            #consequence
            pass
        elif self.current_state == "match_end":
            #consequence
            pass
    
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
        self.image = pygame.Surface((20, 100))
        self.image.fill("white")
        self.rect = self.image.get_frect(center=(100, WINDOW_HEIGHT / 2))
        self.speed = 300
        self.velocity = None
        self.direction = None
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.velocity = self.direction * self.speed
        self.rect.centery += self.velocity * dt
        self.speed = 500
        self.velocity = None
        self.direction = None
        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

class AiPaddle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 100))
        self.image.fill("white")
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH - 100, WINDOW_HEIGHT / 2))
        self.speed = 500
        self.var_speed = 500
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        diff = game.ball.rect.centery - self.rect.centery
        if abs(diff) > 3:
            self.var_speed = min(abs(diff), self.speed) + 400
            self.direction = 1 if diff > 0 else -1
            self.velocity = self.direction * self.var_speed
            self.rect.centery += self.velocity * dt
        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20)) # create a blank 15x15 canvas
        self.image.fill("white") # paint it white - this is the visible ball
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) # get a rect from the surface, centered on screen - this is the ball's position
        self.speed = None
        self.speed_multiplier = 1
        self.velocity = None
        self.mask = pygame.mask.from_surface(self.image)

    def launch(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.speed = 1000
        self.velocity = pygame.Vector2(choice([-0.5, 0.5]), uniform(-0.5, 0.5)) * self.speed # random left or right, slight random vertical angle

    def update(self, dt):
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.velocity.y *= -1
            self.rect.bottom = WINDOW_HEIGHT
        elif self.rect.top <= 0:
            self.velocity.y *= -1
            self.rect.top = 0
        self.rect.center += self.velocity  * game.ball.speed_multiplier * dt

        if game.ball.rect.left <= 0 or game.ball.rect.left >= WINDOW_WIDTH:
            self.kill()
            game.point_start = game.current_time
            game.current_state = "point_start"

class ScoreTracker(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((10, 30))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, 30))

    def update(self, dt):
        text_surf = font.render(str(f"SCORE: {game.cur_score}"), True, (240, 240, 240))
        text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 4, WINDOW_HEIGHT - 50))
        window.blit(text_surf, text_rect)


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
    game.all_sprites.draw(window)

def collisions():
    collision_sprites = pygame.sprite.spritecollide(game.ball, game.paddle_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        for i in collision_sprites:
            if game.ball.velocity.x > 0:
                game.ball.rect.right = i.rect.left
                game.ball.velocity.x *= -1
                game.ball.velocity.y = game.ball.velocity.y * 0.5 + (game.ball.rect.centery - i.rect.centery) * 5
                game.ball.speed_multiplier += 0.05
                beep_sound.play()
                game.cur_score += 1
            elif game.ball.velocity.x < 0:
                game.ball.rect.left = i.rect.right
                game.ball.velocity.x *= -1
                game.ball.velocity.y = game.ball.velocity.y * 0.5 + (game.ball.rect.centery - i.rect.centery) * 5
                game.ball.speed_multiplier += 0.05
                beep_sound.play()
                game.cur_score += 1
            elif game.ball.velocity.y > 0:
                game.ball.rect.bottom = i.rect.top
                game.ball.velocity.y *= -1
                beep_sound.play()
            elif game.ball.velocity.y < 0:
                game.ball.rect.top = i.rect.bottom
                game.ball.velocity.y *= -1
                beep_sound.play()

def update_game(dt):
    pass

def input_handling(event, dt):
    if event.type == pygame.KEYDOWN and game.current_state == "splash":
        game.state(dt)
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT:
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
one_sound = pygame.mixer.Sound(join(BASE_DIR, "audio", "1.wav"))
one_sound.set_volume(0.2)
two_sound = pygame.mixer.Sound(join(BASE_DIR, "audio", "2.wav"))
two_sound.set_volume(0.2)
three_sound = pygame.mixer.Sound(join(BASE_DIR, "audio", "3.wav"))
three_sound.set_volume(0.2)
GO_sound = pygame.mixer.Sound(join(BASE_DIR, "audio", "GO.wav"))
GO_sound.set_volume(0.3)
beep_sound = pygame.mixer.Sound(join(BASE_DIR, "audio", "beeep.ogg"))
beep_sound.set_volume(0.1)
beeeeeep_sound = pygame.mixer.Sound(join(BASE_DIR, "audio", "peeeeeep.ogg"))
beeeeeep_sound.set_volume(0.1)
game_music = pygame.mixer.Sound(join(BASE_DIR, "audio", "two_left_socks.ogg"))
game_music.set_volume(0.2)
game_music.play(loops=-1)

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while game.app_running:
    dt = clock.tick(60) / 1000
    game.current_time = pygame.time.get_ticks()
    window.fill("black")

    for event in pygame.event.get(): # if input events happen (keyboard, mouse etc)
        input_handling(event, dt)

    if game.current_state == "splash":
        draw_splash()
    elif game.current_state == "point_start":
        game.state(dt)
        draw_game(dt)
    elif game.current_state == "in_play":
        game.state(dt)
        draw_game(dt)
    elif game.current_state == "match_end":
        draw_match_end()
    else:
        draw_game(dt)

    pygame.display.update()

pygame.quit()