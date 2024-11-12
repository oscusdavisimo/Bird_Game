import pygame as pg
import random
import math

SCREEN_WIDTH = 1780
SCREEN_HEIGHT = 720

class Player(pg.sprite.Sprite):
    def __init__(self, type, up, down, left, right):
        super().__init__()
        self.type = type
        self.dictionary = {0: "plane.png", 1: "ufo.png"}
        self.surf = pg.image.load(self.dictionary[type])
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def update(self, key):
        if key[self.up]:
            self.rect.move_ip(0, -5)
        if key[self.down]:
            self.rect.move_ip(0, 5)
        if key[self.left]:
            self.rect.move_ip(-5, 0)
        if key[self.right]:
            self.rect.move_ip(5, 0)

        #keep on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pg.sprite.Sprite):
    def __init__(self, type, score):
        super().__init__()
        self.type = type
        self.dictionary = {0: "fiskmås.png", -1: "flamingo.png", 1: "cow.png"}
        self.original_surf = pg.image.load(self.dictionary[type])
        self.surf= self.original_surf.copy()
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(center= (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                                                random.randint(0, SCREEN_HEIGHT)))
        self.speed =  random.randint((3+int(score/5000))-2*type, (10+int(score/5000))-3*type)
        self.angle = 0
        self.rotation = random.randrange(-25, 26, 5)
        self.new_rotation = self.rotation

    def update(self):
        if self.type == 1:
            self.angle += 5
            self.surf = pg.transform.rotate(self.original_surf, self.angle)
            self.rect = self.surf.get_rect(center=self.rect.center)
            self.rect.move_ip(0, self.speed*math.sin(self.rotation))

        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rotation = self.rotation + 270
        if self.rect.top < 0:
            self.rotation = self.rotation + 270

class Cloud(pg.sprite.Sprite):
    def __init__(self, score):
        super().__init__()
        self.surf = pg.image.load("Clouds.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                                               random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(1+int(score/5000), 4+int(score/5000))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()