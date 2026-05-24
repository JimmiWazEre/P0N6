"""

=============================================================
P0N6 FL1P!
=============================================================
Original Pong is boring. P0N6 FL1P! flips the objective:
instead of beating a dumb AI, you work WITH it to keep the
longest rally possible.

The AI's limitations are something to compensate for. Set up 
good returns, control your angles, and keep the rally alive 
as long as you can.

The ball speeds up with every hit. How long can you last?

-------------------------------------------------------------
CONTROLS
-------------------------------------------------------------
Arrow keys      Move paddle
ESC             Pause / unpause
R               Restart (game over screen)
Q               Quit

-------------------------------------------------------------
REFERENCES
-------------------------------------------------------------
pygame-ce docs      https://pyga.me/docs/

"""

import pygame
from os.path import dirname, abspath
from random import uniform, choice, randint

from modules.leaderboard import load_scores, insert_high_score, display_leaderboard, enter_name
from modules.powerup import spawn_powerups, handle_powerup_collisions

BASE_DIR = dirname(abspath(__file__))

# setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
pygame.display.set_caption("P0N6 FL1P!")

# assets
from modules.assets import init_assets
init_assets()
from modules.assets import (
    splash_surf,
    font, font_large,
    one_sound, two_sound, three_sound, GO_sound,
    beep_sound, game_music
)
game_music.play(loops=-1)

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class GameState():
    def __init__(self):
        # app
        self.app_running = True
        self.previous_state = None
        self.current_time = None

        # leaderboard - persists across resets
        self.new_score_index = None
        self.scores = load_scores()

        # sprite groups - persists across resets
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()

        # powerups
        self.active_powerup = []
        self.powerup = None
        self.shield_side = None
        self.shield_x = None

        # initialise game state
        self.reset()
        self.current_state = "splash"

    def reset(self):
        # gameplay
        self.cur_score = 0
        self.final_score = 0
        self.last_countdown = None
        self.point_start = pygame.time.get_ticks()
        self.current_state = "point_start"

        # leaderboard
        self.entering_name = False
        self.pending_name = ""

        # sprites
        self.all_sprites.empty()
        self.paddle_sprites.empty()
        self.ball_sprites.empty()
        self.powerup_sprites.empty()
        self.ball = None
        self.player = None
        self.ai = None
        self.score = ScoreTracker(self.all_sprites)
        self.paddle_len = 100

        # powerups
        self.active_powerup = []
        self.powerup = None
        self.shield_side = None
        self.shield_x = None

    def rebuild_paddles(self):
        player_y = self.player.rect.centery if self.player else WINDOW_HEIGHT / 2
        ai_y = self.ai.rect.centery if self.ai else WINDOW_HEIGHT / 2
        if self.player:
            self.player.kill()
        if self.ai:
            self.ai.kill()
        self.player = PlayerPaddle(self, self.all_sprites, self.paddle_sprites)
        self.ai = AiPaddle(self, self.all_sprites, self.paddle_sprites)
        self.player.rect.centery = player_y
        self.ai.rect.centery = ai_y
        self.player.mask = pygame.mask.from_surface(self.player.image)
        self.ai.mask = pygame.mask.from_surface(self.ai.image)

    def state(self, dt):
        # splash state active
        if self.current_state == "splash":
            self.point_start = self.current_time
            self.current_state = "point_start"

        # point_start state active
        elif self.current_state == "point_start":
            if self.player:
                self.player.kill()
            if self.ai:
                self.ai.kill()
            handle_point_start()

        # in_play state active
        elif self.current_state == "in_play":
            self.player.update(dt)
            self.ai.update(dt)
            self.score.update()
            self.ball.update(dt)
            handle_collisions()
            for p in list(game.active_powerup):
                p.update(game, dt)
            game.powerup_sprites.update(game, dt)

        # game_over state active
        elif self.current_state == "game_over":
            display_leaderboard(game, font, window, WINDOW_WIDTH, WINDOW_HEIGHT)
            prompt_surf = font.render("Press R to play again, or Q to quit", True, (240, 240, 240))
            prompt_rect = prompt_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150))
            show_prompt = (pygame.time.get_ticks() // 500) % 2 == 0
            if show_prompt and not self.entering_name:
                window.blit(prompt_surf, prompt_rect)

# sprite classes

class PlayerPaddle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, game.paddle_len))
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
        self.rect.clamp_ip(clamp)

class AiPaddle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, game.paddle_len))
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
        self.rect.clamp_ip(clamp)

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
            if not self.velocity:
                return
            # move the ball
            effective_multiplier = min(game.ball.speed_multiplier, 3.0)
            self.rect.center += self.velocity * effective_multiplier * dt

            # top and bottom wall bounces
            if self.rect.bottom >= WINDOW_HEIGHT:
                self.velocity.y *= -1
                self.rect.bottom = WINDOW_HEIGHT
            elif self.rect.top <= 0:
                self.velocity.y *= -1
                self.rect.top = 0

            # shield bounces
            if game.shield_side == "right" and game.shield_x and self.velocity.x > 0 and self.rect.right >= game.shield_x:
                self.velocity.x *= -1
                self.rect.right = game.shield_x
            elif game.shield_side == "left" and game.shield_x and self.velocity.x < 0 and self.rect.left <= game.shield_x + 10:
                self.velocity.x *= -1
                self.rect.left = game.shield_x + 10

            # scoring boundary check
            if game.ball.rect.left <= 0 or game.ball.rect.left >= WINDOW_WIDTH:
                self.kill()
                game.final_score = game.cur_score
                game.cur_score = 0
                game.current_state = "game_over"
                insert_high_score(game)

class ScoreTracker(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((10, 30))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, 30))

    def update(self):
        text_surf = font.render(f"SCORE: {game.cur_score}", True, (240, 240, 240))
        text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 4, WINDOW_HEIGHT - 50))
        window.blit(text_surf, text_rect)

# -------------------------------------------------------------
# draw functions
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
    pygame.draw.rect(window, "white", pygame.Rect(25, 0, WINDOW_WIDTH - 50, WINDOW_HEIGHT), 2)
    dash_height = 20
    gap_height = 15
    x = WINDOW_WIDTH // 2 - 1
    y = 2
    while y < WINDOW_HEIGHT:
        pygame.draw.rect(window, "white", pygame.Rect(x, y, 2, dash_height))
        y += dash_height + gap_height

def draw_powerup_timers():
    if not game.active_powerup:
        return
    border_left = 25
    border_right = WINDOW_WIDTH - 25
    padding = 10
    total_width = border_right - border_left - (padding * 2)
    bar_width = (total_width - (padding * 3)) // 4
    bar_height = 10
    y = padding
    for idx, p in enumerate(game.active_powerup):
        x = border_left + padding + idx * (bar_width + padding)
        ratio = 1 - (p.timer / p.duration)
        filled_width = int(bar_width * ratio)
        pygame.draw.rect(window, (60, 60, 60), pygame.Rect(x, y, bar_width, bar_height))
        pygame.draw.rect(window, "chartreuse", pygame.Rect(x, y, filled_width, bar_height))
        label = font.render(type(p).__name__, True, (240, 240, 240))
        window.blit(label, label.get_frect(topleft=(x, y + bar_height + 3)))

def draw_sprites():
    game.all_sprites.draw(window)

# -------------------------------------------------------------
# game functions
# -------------------------------------------------------------

def handle_collisions():
    collision_sprites = pygame.sprite.spritecollide(game.ball, game.paddle_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        for i in collision_sprites:
            # ball moving right - hitting face of AI paddle
            if game.ball.velocity.x > 0:
                game.ball.rect.right = i.rect.left
                game.ball.velocity.x *= -1
                game.ball.velocity.y = game.ball.velocity.y * 0.5 + (game.ball.rect.centery - i.rect.centery) * 5
                game.ball.speed_multiplier += 0.02
                beep_sound.play()
                game.cur_score += 1
                if not game.active_powerup:
                    game.shield_side = "left"
                if randint(1, 10) == 1:
                    spawn_powerups(game, WINDOW_WIDTH, WINDOW_HEIGHT)

            # ball moving left - hitting face of player paddle
            elif game.ball.velocity.x < 0:
                game.ball.rect.left = i.rect.right
                game.ball.velocity.x *= -1
                game.ball.velocity.y = game.ball.velocity.y * 0.5 + (game.ball.rect.centery - i.rect.centery) * 5
                game.ball.speed_multiplier += 0.02
                beep_sound.play()
                game.cur_score += 1
                if not game.active_powerup:
                    game.shield_side = "right"
                if randint(1, 10) == 1:
                    spawn_powerups(game, WINDOW_WIDTH, WINDOW_HEIGHT)

            # ball moving down - hitting top edge of a paddle
            elif game.ball.velocity.y > 0:
                game.ball.rect.bottom = i.rect.top
                game.ball.velocity.y *= -1
                beep_sound.play()

            # ball moving up - hitting bottom edge of a paddle
            elif game.ball.velocity.y < 0:
                game.ball.rect.top = i.rect.bottom
                game.ball.velocity.y *= -1
                beep_sound.play()

    collision_sprites = pygame.sprite.spritecollide(game.ball, game.powerup_sprites, False, pygame.sprite.collide_mask)
    for i in collision_sprites:
        handle_powerup_collisions(i, game)


def handle_input(event, dt):
    # splash state - any key pressed
    if event.type == pygame.KEYDOWN and game.current_state == "splash":
        game.state(dt)

    # Q or window close - quit (unless a prior state has intercepted the keypress)
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT:
        game.app_running = False

    # game_over state - enter name, then restart game
    elif event.type == pygame.KEYDOWN and game.current_state == "game_over":
        if game.entering_name:
            enter_name(event, game)
        elif event.key == pygame.K_r:
            game.reset()
    
    # ESC pressed - pause/unpause (checked independently of other conditions)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        if not game.current_state == "paused":
            game.previous_state = game.current_state
            game.current_state = "paused"
        else:
            game.current_state = game.previous_state

def handle_point_start():
    elapsed = pygame.time.get_ticks() - game.point_start
    prev_flag = None

    # run countdown
    for start, text, sound, flag in countdown:
        if elapsed >= start and elapsed < start + 1000:
            text_surf = font_large.render(text, True, (240, 240, 240))
            text_rect = text_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
            window.blit(text_surf, text_rect)
            if game.last_countdown == prev_flag:
                sound.play()
                game.last_countdown = flag
            break
        prev_flag = flag
    
    # set up for in_play state
    else:
        game.ball = Ball(game.all_sprites, game.ball_sprites)
        game.ai = AiPaddle(game, game.all_sprites, game.paddle_sprites)
        game.player = PlayerPaddle(game, game.all_sprites, game.paddle_sprites)
        game.ball.launch()
        game.current_state = "in_play"

    # for/else: runs only if the loop completed without hitting a break
    # meaning all countdown entries have been passed - transition to in_play

# -------------------------------------------------------------
# game running
# -------------------------------------------------------------

game = GameState()
game.window = window
game.WINDOW_WIDTH = WINDOW_WIDTH
game.WINDOW_HEIGHT = WINDOW_HEIGHT
clock = pygame.time.Clock()
clamp = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
countdown = [(0, "3", three_sound, 1), (1000, "2", two_sound, 2), (2000, "1", one_sound, 3), (3000, "GO!", GO_sound, None)]

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while game.app_running:
    dt = clock.tick(60) / 1000
    game.current_time = pygame.time.get_ticks()
    window.fill("black")

    for event in pygame.event.get(): # if input events happen (keyboard, mouse etc)
        handle_input(event, dt)

    if game.current_state == "splash":
        draw_splash()
    elif game.current_state == "point_start":
        game.state(dt)
        draw_sprites()
    elif game.current_state == "in_play":
        game.state(dt)
        draw_sprites()
        draw_background()
        draw_powerup_timers()
    elif game.current_state == "paused":
        draw_sprites()
        draw_background()
    elif game.current_state == "game_over":
        game.state(dt)

    pygame.display.update()

pygame.quit()