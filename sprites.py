# Sprite classes for platform game
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform or the ground
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20
        hits = pg.sprite.spritecollide(self, self.game.ground, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if keys[pg.K_LSHIFT]:
                self.acc.x = -PLAYER_ACC*2
            else:
                self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            if keys[pg.K_LSHIFT]:
                self.acc.x = PLAYER_ACC*2
            else:
                self.acc.x = PLAYER_ACC
        if keys[pg.K_a]:
            if keys[pg.K_LSHIFT]:
                self.acc.x = -PLAYER_ACC*2
            else:
                self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            if keys[pg.K_LSHIFT]:
                self.acc.x = PLAYER_ACC*2
            else:
                self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # stops the player from going above the top of the screen
        if self.pos.y <= 20:
            self.pos.y = 20
            self.vel.y = 0
        # stops the player from going outside the left and right of the screen
        if self.pos.x > WIDTH-15:
            self.pos.x = WIDTH-15
            self.vel.x = 0
        if self.pos.x < 15:
            self.pos.x = 0+15
            self.vel.x = 0

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        #shotgun level
        #self.rect.x-=2
        #if self.rect.right <= 0:
        #    self.rect.x += 600
        #machine gun level
        self.rect.x-=2
        if self.rect.right <= 0:
            self.rect.x += random.randrange(600, 700)
            self.rect.y += random.randrange(-50, 50)
        

class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

