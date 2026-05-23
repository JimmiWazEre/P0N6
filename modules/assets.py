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

def init_assets():
    global splash_surf, big_ball_surf, slow_ball_surf, shield_surf, big_paddle_surf
    global font, font_large
    global one_sound, two_sound, three_sound, GO_sound
    global beep_sound, beeeeeep_sound, game_music, powerup_sound

    # images
    splash_surf = pygame.image.load(join(ASSETS_DIR, "images", "splash.png")).convert()
    big_ball_surf = pygame.image.load(join(ASSETS_DIR, "images", "sized_BigBall.png")).convert_alpha()
    slow_ball_surf = pygame.image.load(join(ASSETS_DIR, "images", "sized_SlowBall.png")).convert_alpha()
    shield_surf = pygame.image.load(join(ASSETS_DIR, "images", "sized_Shield.png")).convert_alpha()
    big_paddle_surf = pygame.image.load(join(ASSETS_DIR, "images", "sized_BigPaddle.png")).convert_alpha()

    # fonts
    font = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 20)
    font_large = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 60)

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