import os.path
import pygame
import json

pygame.init()

# other settings
if os.path.exists('settings.json'):
    with open('settings.json', 'r') as file:
        data = json.load(file)
        FPS = data['fps']
        SOUNDS = data['sounds']
else:
    FPS = 144
    SOUNDS = True

if FPS == 60:
    BACK_SPEED = 1 * 2.4
    SHIP_SPEED = 3 * 2.4
    LASER_SPEED = 5 * 2.4
    ENEMY_SPEED = 3.5 * 2.4
else:
    BACK_SPEED = 1
    SHIP_SPEED = 3
    LASER_SPEED = 5
    ENEMY_SPEED = 3.5

PASSING_GAME_SCORE = 150

COLORS = {'black': (0, 0, 0), 'white': (255, 255, 255)}

# window settings
WIDTH = 640
HEIGHT = 480
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

CAPTION = 'Space Adventures'

# back settings
BACK_IMG = pygame.transform.scale(pygame.image.load('sprites/space.png'), (640, 480))
y_back = 0

# sound settings
killed_sound = pygame.mixer.Sound('sounds/killed_sound.mp3')
shot_sound = pygame.mixer.Sound('sounds/shot_sound.mp3')
engine_sound = pygame.mixer.music.load('sounds/engine_sound.mp3')

# font settings
font = pygame.font.Font('font/GorgeousPixel.ttf', 30)

# starting position of the player
STARTING_X = 260
STARTING_Y = 320

# ship settings
SHIP_WIDTH = 90
SHIP_HEIGHT = 120

# laser settings
LASER_PLUS_X = 42
LASER_PLUS_Y = 43

LASER_X = STARTING_X + LASER_PLUS_X
LASER_Y = STARTING_Y + LASER_PLUS_Y
LASER_WIDTH = 5
LASER_HEIGHT = 30

# enemy settings
ENEMY_WIDTH = 80
ENEMY_HEIGHT = 120
