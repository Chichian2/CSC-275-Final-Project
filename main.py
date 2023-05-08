import pygame as pg
import random
import os
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.paused = False
        self.move_background = 0
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.levels =['level1.txt','level3.txt','level2.txt']
        self.level = 0
        self.show_start_screen()
        #self.start = True
        self.load_data()

    def load_data(self):
        print("load data")
        game_folder = path.dirname(__file__)
        level_folder = path.join(game_folder,'level')
        self.img_folder = path.join(game_folder,'img')
        self.item_folder = path.join(self.img_folder,'Items')
        self.map_data = []
        self.map_data.clear()
        with open(path.join(level_folder, self.levels[self.level]), 'rt') as f:
            print(f)
            for line in f:
                self.map_data.append(line.replace('\n',''))
        self.new()

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.boss_sprite = pg.sprite.Group()
        self.player = Player(self)
        #Hearts
        a1 = Hearts(10,10,1, self)
        a2 = Hearts(10,40,2, self)
        a3 = Hearts(10,70,3, self)
        self.all_sprites.add(a1)
        self.all_sprites.add(a2)
        self.all_sprites.add(a3)

        self.background_img = pg.image.load(path.join(self.img_folder, 'Background.png'))
        self.background_with_size = pg.transform.scale(self.background_img, (5*3076, 5*128))
        self.all_sprites.add(self.powerups)
        self.all_sprites.add(self.player)

        self.bossTime = False
        self.bulletTimers = []
        
        for ground in GROUND:
            g = Ground(*ground)
            self.all_sprites.add(g)
            self.ground.add(g)
        print(self.map_data[1])
        print(self.map_data)
        self.distance = int(self.map_data[3])
        self.text = self.map_data[3].rjust(3)
        self.font = pg.font.SysFont('Consolas', 30)
        pg.time.set_timer(pg.USEREVENT, 1000)
        if self.map_data[1] == "MachineGun":
            print("worked")
            for plat in MGPLATFORM_LIST:
                p = Platform(*plat,self,"Machine_Gun")
                self.all_sprites.add(p)
                self.platforms.add(p)
        elif self.map_data[1] == "ShotGun":
            for plat in SGPLATFORM_LIST:
                p = Platform(*plat,self,"Shot_Gun")
                self.all_sprites.add(p)
                self.platforms.add(p)
        elif self.map_data[1] == "CrossBow":
            for plat in CBPLATFORM_LIST:
                p = Platform(*plat,self,"Cross_Bow")
                self.all_sprites.add(p)
                self.platforms.add(p)
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.spawnrate = int(self.map_data[2])
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.platforms.update()
        # check if player hits a platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.bottom + 40
                self.player.vel.y = 0

        #check if player hits the ground
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.ground, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.ground, False)
            if hits:
                self.player.pos.y = hits[0].rect.bottom + 40
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.USEREVENT:
                self.text = str(self.distance).rjust(3)
                if self.distance == 0 and not self.bossTime:
                    self.boss = Boss(self.map_data[1],self)
                    self.boss_sprite.add(self.boss)
                    self.all_sprites.add(self.boss_sprite)
                    self.bossTime = True
                else:
                    if self.distance > 0 and not self.paused:
                        self.distance -= 1
                    else:
                        for i, timers in enumerate(self.bulletTimers):
                            self.bulletTimers[i] = timers - 1
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                    self.start = False

    def draw(self):
        # Game Loop - draw
        self.screen.blit(self.background_with_size, (self.move_background, 0))
        if (self.move_background >= -13000) and (not self.paused):
            self.move_background -= 1
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.font.render(self.text, True, (255, 255, 255)), (32, 48))
        self.screen.blit(pg.image.load(path.join(self.item_folder, 'Grappling_Hook.png')), (100, 20))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 12).render(str(self.player.grappling_hook_count), True, WHITE, None), (115, 30))        
        self.screen.blit(pg.image.load(path.join(self.item_folder, 'Double_Jump.png')), (150, 20))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 12).render(str(self.player.double_jump_count), True, WHITE, None), (165, 30))         
        self.screen.blit(pg.image.load(path.join(self.item_folder, 'Sheild.png')), (200, 20))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 12).render(str(self.player.bullet_shield_count), True, WHITE, None), (215, 30))
        # draws line for grappling hook
        if self.player.movingx:
            pg.draw.line(self.screen,BLUE,(self.player.pos.x,self.player.pos.y),(self.player.tempx,self.player.tempy),6)
        #pause game
        if self.paused and not self.start:
            self.screen.blit(self.dim_screen, (0,0))
            self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Continue? Press P', True, WHITE, None), (WIDTH/8, HEIGHT/2))
        elif self.paused and self.start:
            self.screen.blit(self.dim_screen, (0,0))
            self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Start? Press P', True, WHITE, None), (WIDTH/8, HEIGHT/5))
            self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Arrow keys and space', True, WHITE, None), (10, HEIGHT/5+100))
            self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('to move. X to use', True, WHITE, None), (10, HEIGHT/5+200))
            self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Grappling hook.', True, WHITE, None), (10, HEIGHT/5+300))
            self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Touch Guns', True, WHITE, None), (10, HEIGHT/5+400))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        #self.screen.blit(self.dim_screen, (0,0))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Start? Press P', True, WHITE, None), (WIDTH/8, HEIGHT/3))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 40).render('Arrow keys and space to move.\n X to use grappling hook.', True, WHITE, None), (WIDTH/8, HEIGHT/3+300))
        self.start = True
        self.paused = True

g = Game()
g.show_start_screen()
while g.running:
    g.new()

pg.quit()
