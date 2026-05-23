# cretation: powerup sounds by TeamAlphaGames https://opengameart.org/content/8-bitnes-powerup-sound-effects

import pygame
from random import randint, choice

from modules.assets import big_ball_surf, slow_ball_surf, shield_surf, big_paddle_surf, powerup_sound

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.pos = pos
        self.duration = 5000
        self.timer = 0
        self.active = False
        self.mask = None
        self.og_speed_multiplier = None
        self.og_paddle_length = None

    def update(self, game, dt):
        if self.active:
            self.timer += dt * 1000
            if self.timer >= self.duration:
                self.expire(game)

class SlowBall(PowerUp):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        self.image = slow_ball_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self, game):
        powerup_sound.play()
        self.timer = 0
        self.active = True
        self.og_speed_multiplier = game.ball.speed_multiplier
        game.ball.speed_multiplier *= 0.5

    def expire(self, game):
        game.powerup = None
        game.ball.speed_multiplier = self.og_speed_multiplier

class BigPaddle(PowerUp):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        self.image = big_paddle_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self, game):
        powerup_sound.play()
        self.timer = 0
        self.active = True
        self.og_paddle_len = game.paddle_len
        game.paddle_len *= 2
        game.rebuild_paddles()

    def expire(self, game):
        game.paddle_len = self.og_paddle_len
        game.rebuild_paddles()
        game.powerup = None

class Shield(PowerUp):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        self.image = shield_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self, game):
        powerup_sound.play()
        self.timer = 0
        self.active = True

    def expire(self, game):
        game.powerup = None

class BigBall(PowerUp):
    def __init__(self, pos, *groups):
        super().__init__(pos, *groups)
        self.image = big_ball_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self, game):
        powerup_sound.play()
        self.timer = 0
        self.active = True

    def expire(self, game):
        game.powerup = None

# -------------------------------------------------------------
# functions
# -------------------------------------------------------------

def spawn_powerups(game, WINDOW_WIDTH, WINDOW_HEIGHT):
    pos = (WINDOW_WIDTH // 2, randint(50, WINDOW_HEIGHT - 50))
    powerup_type = choice([SlowBall, BigPaddle, Shield, BigBall])
    game.powerup = powerup_type(pos, game.powerup_sprites)

def handle_powerup_collisions(game):
    pass
