from settings import *
from classes import Player, Enemy
from random import randint
import pygame
import json
import os
import sys

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

clock = pygame.time.Clock()

running = False

player = Player(STARTING_X, STARTING_Y, SHIP_WIDTH, SHIP_HEIGHT)

left = False
right = False

back_imgs = [{'x': 0, 'y': y_back}, {'x': 0, 'y': y_back - 480}]

enemies = []


# function to randomize the position of enemy
def create_enemies(n):
    first_x = randint(0, 100)
    second_x = randint(210, 310)
    third_x = randint(420, 520)
    x_pos = [first_x, second_x, third_x]
    for _ in range(n):
        enemies.append(Enemy(x_pos.pop(randint(0, len(x_pos)-1)), -ENEMY_HEIGHT))


create_enemies(randint(2, 3))

score = 0

paused = False
stopped = False

TEXT_X = 70
TEXT_Y = 20


# draw text on screen
def draw_text(surface, text, color, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = x, y
    surface.blit(text_obj, text_rect)


# loading best score from json
def load_best_score(filename):
    with open(filename, 'r') as file:
        return json.load(file)['best_score']


# checks best score or creates data.json if not exists
if os.path.exists('data.json'):
    best_score = load_best_score('data.json')
else:
    with open('data.json', 'w') as file:
        data = {
            'best_score': 0,
            'passed_game': False
        }
        best_score = 0
        json.dump(data, file)


# writing new score in json
def update_json(score, passed=None):
    with open('data.json', 'r') as file:
        data = json.load(file)
        if data['best_score'] < round(score):
            data['best_score'] = round(score)
        if passed:
            data['passed_game'] = True

    with open('data.json', 'w') as file:
        json.dump(data, file)


# loop before the game
while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            running = True

    draw_text(win, 'Press any key to start', COLORS['white'],
              HALF_WIDTH, HALF_HEIGHT)

    pygame.display.flip()
    clock.tick(FPS)

# game loop
while running:
    if back_imgs[1]['y'] > 0:
        back_imgs.append({'x': 0, 'y': y_back - 480})
        back_imgs.remove(back_imgs[0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                right = False
                left = True

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                left = False
                right = True

            elif event.key == pygame.K_SPACE and not stopped and not player.shooting and not paused:
                shot_sound.play()
                player.shooting = True

            elif event.key == pygame.K_ESCAPE and not stopped:
                if not paused:
                    paused = True
                else:
                    paused = False

            elif event.key == pygame.K_SPACE and stopped:
                score = 0
                enemies.clear()
                player.rect = pygame.Rect((STARTING_X, STARTING_Y), (SHIP_WIDTH, SHIP_HEIGHT))
                player.laser_rect = pygame.Rect((LASER_X, LASER_Y), (LASER_WIDTH, LASER_HEIGHT))
                best_score = load_best_score('data.json')
                stopped = False
                paused = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = False

    if not stopped and not paused:
        if SOUNDS:
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        if FPS == 144:
            score += 0.005
        else:
            score += 0.005 * 2.4

        if right:
            player.move(direction='right')
        elif left:
            player.move(direction='left')

        if player.shooting:
            player.shoot()

        for img in back_imgs:
            img['y'] += BACK_SPEED
            win.blit(BACK_IMG, (img['x'], img['y']))

        if len(enemies) == 0:
            create_enemies(randint(2, 3))

        for enemy in enemies:
            if enemy.rect.y < HEIGHT:
                enemy.move()
            else:
                enemies.remove(enemy)

            win.blit(enemy.img, (enemy.rect.x, enemy.rect.y))

            if enemy.rect.colliderect(player.rect):
                stopped = True
                draw_text(win, 'You lose! Press Space to restart', COLORS['white'], HALF_WIDTH, HALF_HEIGHT)
                update_json(score)

            if player.laser_rect.colliderect(enemy.rect):
                if SOUNDS:
                    killed_sound.play()
                enemies.remove(enemy)

        if round(score) < 10:
            TEXT_X = 70
            TEXT_Y = 20

        elif round(score) < 100:
            if round(score) == 10:
                TEXT_X += 10
                score += 1

        elif round(score) == 100:
            TEXT_X += 10
            score += 1

        if round(score) == PASSING_GAME_SCORE:
            stopped = True
            draw_text(win, 'You passed the game! Congratulations!', COLORS['white'], HALF_WIDTH, HALF_HEIGHT)
            update_json(score, passed=True)

    if stopped or paused and SOUNDS:
        pygame.mixer.music.stop()

    if paused:
        draw_text(win, 'The game is paused', COLORS['white'], HALF_WIDTH, HALF_HEIGHT)
        draw_text(win, 'Press Escape to continue', COLORS['white'], HALF_WIDTH, HALF_HEIGHT+30)

    draw_text(win, f'Score: {round(score)}', COLORS['white'],  TEXT_X, TEXT_Y)
    draw_text(win, f'Best score: {best_score}', COLORS['white'], WIDTH-120, 20)

    win.blit(player.laser_img, player.laser_rect)
    win.blit(player.img, player.rect)

    clock.tick(FPS)
    pygame.display.flip()
