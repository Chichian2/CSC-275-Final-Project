# Sprite classes for platform game
import pygame as pg
import random
import time
import os
from os import path
import math
import pytweening as tween
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        #power up items
        self.powerup = []

        #player's hp
        self.health = 3

        #for animation
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pg.time.get_ticks()
        self.in_air=False
        self.moving_left = False
        self.moving_right = False

        #load all images for player
        scale=2
        animation_types = ['Idle', 'RunR', 'RunL','Jump','Grappling']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in files in the folder
            num_of_frames = len(os.listdir(f'img/player/{animation}'))
            for i in range(num_of_frames):
                img = pg.image.load(f'img/player/{animation}/{i}.png').convert_alpha()
                img = pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)



        #variables for grappling hook.
        self.movingx = False
        self.movingy = False
        self.tempx = self.pos.x
        self.tempy = self.pos.y
        self.distx = 0
        self.disty = 0

    def grappling_math(self):
        self.powerup.remove("Grappling_Hook")
        self.tempx = self.pos.x
        self.tempy = self.pos.y
        length = RANGE
        for plat in self.game.platforms:
            self.acc.y = 0
            # condition that was on if statement plat.rect.x > self.tempx and plat.rect.x < self.pos.x + 200
            if (plat.rect.x + plat.width/2) > self.pos.x and (plat.rect.x + (plat.width/2)) < WIDTH and plat.rect.y < self.pos.y:
                lengthx = ((plat.rect.x + (plat.width/2)) - self.pos.x)
                lengthy = (self.pos.y - (plat.rect.y + 60))
                if(math.sqrt((lengthx**2) + (lengthy**2)) <= length):
                    length = math.sqrt((lengthx**2) + (lengthy**2))
                    self.tempx = plat.rect.x + (plat.width/2)
                    self.tempy = plat.rect.y + plat.height
                    print(plat)
        print(self.tempx)
        print(self.tempy) 
        if self.pos.x < self.tempx:
            self.movingx = True
            self.distx = (self.tempx - self.pos.x) * SPEEDMULT
            #self.update()
            #pg.time.wait(5)
        if self.pos.y > self.tempy + 60:
            self.disty = (self.pos.y - (self.tempy + 60)) * SPEEDMULT
            self.acc.y = 0
            self.movingy = True
        #    self.pos.y -= 1
        #    self.rect.midbottom = self.pos

    def collide_with_powerup(self):
        game_folder = path.dirname(__file__)
        snd_folder = path.join(game_folder, 'snd')
        
        self.effects_sounds = {}
        for type in EFFECT_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECT_SOUNDS[type]))
            
        hits = pg.sprite.spritecollide(self, self.game.powerups, True)
        if hits:
            if hits[0].typ == "Health":
                if self.health == 1:
                    #insert sound for Health pick up
                    self.health +=1
                    a2 = Hearts(10,40,2, self.game)
                    self.game.all_sprites.add(a2)
                elif self.health == 2:
                    #insert sound for Health pick up
                    self.health +=1
                    a3 = Hearts(10,70,3, self.game)
                    self.game.all_sprites.add(a3)
                else:
                    self.effects_sounds['Health'].play()
                return
            elif hits[0].typ == "Grappling_Hook":
                self.effects_sounds['Grappling_Hook'].play()
            elif hits[0].typ == "Double_Jump":
                self.effects_sounds['Double_Jump'].play()
            elif hits[0].typ == "Bullet_Shield":
                self.effects_sounds['Bullet_Shield'].play()
            self.powerup.append(hits[0].typ)
            print(str(self.powerup))

    def deal_damage(self):
        print(self.health)
        self.health-=1
        if self.health <= 0:
            self.effects_sounds['Death'].play()
            time.sleep(2)
            if self.game.playing:
                    self.game.playing = False
            self.game.running = False

    #Checks collision to see if player takes damage
    def take_damage(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            for hit in hits:
                if hit.rect.x > self.rect.x+10:
                    if self.rect.y < (hit.rect.y + hit.height/2) and self.rect.y > (hit.rect.y - hit.height/2):
                        self.pos.y = hit.rect.y-50
                        self.effects_sounds['Damage'].play()
                        if "Bullet_Shield" in self.powerup:
                            print("worked")
                            self.powerup.remove("Bullet_Shield")
                            return
                        self.deal_damage()
                        break
                
    def fall(self):
        if self.rect.y >= HEIGHT:
            obj = random.choice(self.game.platforms.sprites())
            if obj.rect.x + obj.width > WIDTH or obj.rect.x < 0:
                self.fall()
            else:
                #self.vel = vac(0,PLAYER_GRAV)
                self.pos = vec(obj.rect.x, obj.rect.y-50)
                self.deal_damage()

    def jump(self):
        # jump only if standing on a platform or the ground or you have double jump power up.
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        hits2 = pg.sprite.spritecollide(self, self.game.ground, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20
        elif hits2:
            self.vel.y = -20
        elif"Double_Jump" in self.powerup:
            self.powerup.remove("Double_Jump")
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.take_damage()
        self.collide_with_powerup()
        self.fall()
        keys = pg.key.get_pressed()
        if keys[pg.K_x] and "Grappling_Hook" in self.powerup:
            self.grappling_math()
        elif keys[pg.K_LEFT]:
            self.moving_left = True
            if keys[pg.K_LSHIFT]:
                self.acc.x = -PLAYER_ACC*2
            else:
                self.acc.x = -PLAYER_ACC
        elif keys[pg.K_RIGHT]:
            self.moving_right = True
            if keys[pg.K_LSHIFT]:
                self.acc.x = PLAYER_ACC*2
            else:
                self.acc.x = PLAYER_ACC
        elif keys[pg.K_a]:
            self.moving_left = True
            if keys[pg.K_LSHIFT]:
                self.acc.x = -PLAYER_ACC*2
            else:
                self.acc.x = -PLAYER_ACC
        elif keys[pg.K_d]:
            self.moving_right = True
            if keys[pg.K_LSHIFT]:
                self.acc.x = PLAYER_ACC*2
            else:
                self.acc.x = PLAYER_ACC
        elif keys[pg.K_t]:
            self.powerup.append("Grappling_Hook")
            self.tempobj = Item(80,80,"Grappling_Hook")
        elif not keys[pg.K_LEFT]:
            self.moving_left = False
        elif not keys[pg.K_RIGHT]:
            self.moving_right= False
        elif not keys[pg.K_a]:
            self.moving_left = False
        elif not keys[pg.K_d]:
            self.moving_right= False

        if self.in_air:
            self.update_action(3)
        elif self.movingx:
            self.update_action(4)
        elif self.moving_left:
            self.update_action(2)
        elif self.moving_right:
            self.update_action(1)
        else:
            self.update_action(0)
        
        if self.pos.x < self.tempx and self.movingx:
            #self.acc.x = PLAYER_ACC
            self.pos.x += self.distx
        if self.pos.y > self.tempy + 60 and self.movingy:
            #self.acc.y = -PLAYER_ACC
            self.acc.y = 0
            self.vel.y = 0
            self.pos.y -= self.disty

        if self.pos.x >= self.tempx and self.movingx:
            self.movingx = False
            self.acc.x = PLAYER_ACC
            self.vel.x = 11
        if self.pos.y <= self.tempy + 65 and self.movingy:
            self.movingy = False
            self.acc.y = PLAYER_GRAV

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
        self.update_animation()


    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h,game,typ):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.width = w
        self.height = h
        self.type =typ

        #for animation
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pg.time.get_ticks()

        scale=2
        bullet_types = ['NBullet']
        for animation in bullet_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in files in the folder
            num_of_frames = len(os.listdir(f'img/Bullet/{animation}'))
            for i in range(num_of_frames):
                img = pg.image.load(f'img/Bullet/{animation}/{i}.png').convert_alpha()
                img = pg.transform.scale(img, (w, h))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def item_spawn(self):
        if random.randrange(1,100) > self.game.spawnrate and self.game.player.powerup != 1:
                    itemSpawned = random.randrange(1,5)
                    if itemSpawned == 1:
                        g = Item(600, self.rect.y - 20,"Grappling_Hook",self.game)
                    if itemSpawned == 2:
                        g = Item(600, self.rect.y - 20,"Double_Jump",self.game)
                    if itemSpawned == 3:
                        g = Item(600, self.rect.y - 20,"Bullet_Shield",self.game)
                    if itemSpawned == 4:
                        g = Item(600, self.rect.y - 20,"Health",self.game)
                    self.game.all_sprites.add(g)
                    self.game.powerups.add(g)

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update(self):
        if not self.game.bossTime:
            #shotgun level
            self.update_animation()
            if self.type == "Shot_Gun":
                self.rect.x-=2
                if self.rect.right <= 0:
                    self.rect.x += 600
                    self.item_spawn()
            #machine gun level
            elif self.type == "Machine_Gun":
                self.rect.x-=2
                if self.rect.right <= 0:
                    self.rect.x += random.randrange(600, 700)
                    self.rect.y += random.randrange(-50, 50)
                    self.item_spawn()
        else:
            self.update_animation()
            self.rect.x -= 2
        

class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w

    def update(self):
        self.rect.x -=2
        if self.rect.x + self.width < 0:
            self.kill()

#Class to handle all Items
class Item(pg.sprite.Sprite):
    def __init__(self, x, y, typ,game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(game.item_folder, ITEM_IMAGE[typ])).convert_alpha()
        self.image = pg.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.center = (x,y)
        self.typ = typ
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        self.move = True

    def update(self):
        if self.move:
            self.rect.centerx-=3
        #bobing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step >= BOB_RANGE:
            self.step = 0
            self.dir *= -1


#sprite for hearts to represent health
class Hearts(pg.sprite.Sprite):
    def __init__(self, x, y, number, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path.join(game.item_folder, 'Heart.png')).convert_alpha()
        self.image = pg.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = number
        self.game = game

    def update(self):
        if self.game.player.health < self.number:
            self.kill()
