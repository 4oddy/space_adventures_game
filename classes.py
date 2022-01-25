from settings import *
import pygame

pygame.init()


class Player:
    def __init__(self, x, y, x1, y1):
        self.rect = pygame.Rect((x, y), (x1, y1))
        self.img = pygame.transform.scale(pygame.image.load('sprites/player.png'), (x1, y1))
        self.laser_rect = pygame.Rect((LASER_X, LASER_Y), (LASER_WIDTH, LASER_HEIGHT))
        self.laser_img = pygame.transform.scale(pygame.image.load('sprites/laser.png'), (5, 30))
        self.shooting = False

    def move(self, direction):
        if direction == 'right' and self.rect.x < WIDTH-100:
            self.rect.x += SHIP_SPEED
            if not self.shooting:
                self.laser_rect.x += SHIP_SPEED

        if direction == 'left' and self.rect.x > 0:
            self.rect.x -= SHIP_SPEED
            if not self.shooting:
                self.laser_rect.x -= SHIP_SPEED

    def shoot(self):
        if self.laser_rect.y > -50:
            self.laser_rect.y -= LASER_SPEED
        else:
            self.shooting = False
            self.laser_rect.x, self.laser_rect.y = (self.rect.x + LASER_PLUS_X, self.rect.y + LASER_PLUS_Y)


class Enemy:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(
            pygame.image.load('sprites/enemy_ship.png'), (ENEMY_WIDTH, ENEMY_HEIGHT)
        )
        self.rect = pygame.Rect((x, y), (ENEMY_WIDTH-4, ENEMY_HEIGHT-20))

    def move(self):
        self.rect.y += ENEMY_SPEED
