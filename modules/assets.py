"""

=============================================================
assets.py
=============================================================
Centralised asset loading for P0N6 FL1P!

All images, fonts, and sounds are declared as module-level
None values and populated by init_assets(), which must be
called after pygame.init() in main.py.

Powerup icon surfaces are generated programmatically via
make_powerup_surf() rather than loaded from image files,
keeping the retro blocky aesthetic consistent.

powerup sounds by TeamAlphaGames 
https://opengameart.org/content/8-bitnes-powerup-sound-effects

-------------------------------------------------------------
USAGE
-------------------------------------------------------------
Call init_assets() once after pygame.init(), then import
the named assets you need:

    from modules.assets import font, beep_sound

"""

import pygame
from os.path import dirname, abspath, join

BASE_DIR = dirname(abspath(__file__))
ASSETS_DIR = dirname(BASE_DIR)  # points to project root, not modules/

# -------------------------------------------------------------
# module-level declarations
# -------------------------------------------------------------

# images
splash_surf = None
big_ball_surf = None
slow_ball_surf = None
shield_surf = None
big_paddle_surf = None

# fonts
font = None
font_large = None

# sounds
one_sound = None
two_sound = None
three_sound = None
GO_sound = None
beep_sound = None
beeeeeep_sound = None
game_music = None
powerup_sound = None

# -------------------------------------------------------------
# init
# -------------------------------------------------------------

def make_powerup_surf(colour, label):
    surf = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.rect(surf, colour, pygame.Rect(0, 0, 60, 60), border_radius=6)
    pygame.draw.rect(surf, "white", pygame.Rect(0, 0, 60, 60), 2, border_radius=6)
    text = font.render(label, True, "white")
    text_rect = text.get_frect(center=(30, 30))
    surf.blit(text, text_rect)
    return surf

def init_assets():
    global splash_surf, big_ball_surf, slow_ball_surf, shield_surf, big_paddle_surf
    global font, font_large
    global one_sound, two_sound, three_sound, GO_sound
    global beep_sound, beeeeeep_sound, game_music, powerup_sound

    # fonts
    font = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 20)
    font_large = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 60)

    # images
    splash_surf = pygame.image.load(join(ASSETS_DIR, "images", "splash.png")).convert()
    big_ball_surf = make_powerup_surf((220, 50, 50), "BB")
    slow_ball_surf = make_powerup_surf((50, 100, 220), "SB")
    shield_surf = make_powerup_surf((220, 180, 50), "S")
    big_paddle_surf = make_powerup_surf((50, 180, 80), "BP")

    # sounds
    one_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "1.wav"))
    one_sound.set_volume(0.5)
    two_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "2.wav"))
    two_sound.set_volume(0.5)
    three_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "3.wav"))
    three_sound.set_volume(0.5)
    GO_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "GO.wav"))
    GO_sound.set_volume(0.8)
    beep_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "beeep.ogg"))
    beep_sound.set_volume(0.1)
    beeeeeep_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "peeeeeep.ogg"))
    beeeeeep_sound.set_volume(0.1)
    game_music = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "two_left_socks.ogg"))
    game_music.set_volume(0.2)
    game_music.play(loops=-1)
    powerup_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "Powerup5.wav"))
    powerup_sound.set_volume(0.2)