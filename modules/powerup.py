# creation: powerup sounds by TeamAlphaGames https://opengameart.org/content/8-bitnes-powerup-sound-effects

import pygame
from random import randint, choice

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.pos = pos
        self.duration = 10000
        self.timer = 0
        self.active = False
        self.mask = None

    def update(self, game, dt):
        if self.active:
            self.timer += dt * 1000
            if self.timer >= self.duration:
                self.expire(game)
        else:
            self.timer += dt * 1000
            if self.timer >= self.duration:
                self.kill()
                game.powerup = None

class SlowBall(PowerUp):
    def __init__(self, pos, *groups):
        from modules.assets import slow_ball_surf
        super().__init__(pos, *groups)
        self.image = slow_ball_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.og_speed_multiplier = None

    def apply(self, game):
        from modules.assets import powerup_sound
        powerup_sound.play()
        self.timer = 0
        self.active = True
        self.og_speed_multiplier = game.ball.speed_multiplier
        game.ball.speed_multiplier *= 0.5

    def expire(self, game):
        self.active = False
        game.ball.speed_multiplier = self.og_speed_multiplier
        game.active_powerup.remove(self)

class BigPaddle(PowerUp):
    def __init__(self, pos, *groups):
        from modules.assets import big_paddle_surf
        super().__init__(pos, *groups)
        self.image = big_paddle_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.og_paddle_len = None

    def apply(self, game):
        from modules.assets import powerup_sound
        powerup_sound.play()
        self.timer = 0
        self.active = True
        self.og_paddle_len = game.paddle_len
        game.paddle_len *= 2
        game.rebuild_paddles()

    def expire(self, game):
        self.active = False
        game.paddle_len = self.og_paddle_len
        game.rebuild_paddles()
        game.active_powerup.remove(self)

class Shield(PowerUp):
    def __init__(self, pos, *groups):
        from modules.assets import shield_surf
        super().__init__(pos, *groups)
        self.image = shield_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self, game):
        from modules.assets import powerup_sound
        powerup_sound.play()
        self.timer = 0
        self.active = True
        game.shield_x = 70 if game.shield_side == "left" else game.WINDOW_WIDTH - 70

    def expire(self, game):
        self.active = False
        game.shield_side = None
        game.shield_x = None
        game.active_powerup.remove(self)

    def update(self, game, dt):
        super().update(game, dt)
        if self.active:
            shield_colour = (0, 150, 255) if (pygame.time.get_ticks() // 250) % 2 == 0 else (0, 0, 100)
            pygame.draw.rect(game.window, shield_colour, pygame.Rect(game.shield_x, 0, 10, game.WINDOW_HEIGHT))

class BigBall(PowerUp):
    def __init__(self, pos, *groups):
        from modules.assets import big_ball_surf
        super().__init__(pos, *groups)
        self.image = big_ball_surf
        self.rect = self.image.get_frect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.og_ball_size = None

    def apply(self, game):
        from modules.assets import powerup_sound
        powerup_sound.play()
        self.timer = 0
        self.active = True
        self.og_ball_size = game.ball.image.get_size()
        new_size = (self.og_ball_size[0] * 2, self.og_ball_size[1] * 2)
        game.ball.image = pygame.Surface(new_size)
        game.ball.image.fill("white")
        game.ball.rect = game.ball.image.get_frect(center=game.ball.rect.center)
        game.ball.mask = pygame.mask.from_surface(game.ball.image)

    def expire(self, game):
        self.active = False
        game.ball.image = pygame.Surface(self.og_ball_size)
        game.ball.image.fill("white")
        game.ball.rect = game.ball.image.get_frect(center=game.ball.rect.center)
        game.ball.mask = pygame.mask.from_surface(game.ball.image)
        game.active_powerup.remove(self)

# -------------------------------------------------------------
# functions
# -------------------------------------------------------------

def spawn_powerups(game, WINDOW_WIDTH, WINDOW_HEIGHT):
    active_types = {type(p) for p in game.active_powerup}
    on_screen_types = {type(s) for s in game.powerup_sprites}
    excluded = active_types | on_screen_types
    available = [t for t in [SlowBall, BigPaddle, Shield, BigBall] if t not in excluded]
    if not available:
        return
    offset = randint(50, 80) * choice([-1, 1])
    pos = (WINDOW_WIDTH // 2 + offset, randint(50, WINDOW_HEIGHT - 50))
    powerup_type = choice(available)
    powerup_type(pos, game.all_sprites, game.powerup_sprites)
   # game.powerup = powerup_type(pos, game.all_sprites, game.powerup_sprites)

def handle_powerup_collisions(i, game):
    if not i.active:
        game.active_powerup.append(i)
       # game.powerup = None
        i.kill()
        i.apply(game)