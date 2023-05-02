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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.levels =['level1.txt','level2.txt']
        self.level = 0
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
        self.player = Player(self)
        #Hearts
        a1 = Hearts(10,10,1, self)
        a2 = Hearts(10,40,2, self)
        a3 = Hearts(10,70,3, self)
        self.all_sprites.add(a1)
        self.all_sprites.add(a2)
        self.all_sprites.add(a3)
        
        self.all_sprites.add(self.powerups)
        self.all_sprites.add(self.player)

        self.bossTime = False
        
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
        self.paused = False
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
                    boss = Boss(self.map_data[1],self)
                    self.all_sprites.add(boss)
                    self.bossTime = True
                else:
                    self.distance -= 1
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.font.render(self.text, True, (255, 255, 255)), (32, 48))
        self.screen.blit(pg.image.load(path.join(self.item_folder, 'Grappling_Hook.png')), (100, 20))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 12).render(str(self.player.grappling_hook_count), True, (255, 255, 255), (0, 0, 0)), (115, 30))        
        self.screen.blit(pg.image.load(path.join(self.item_folder, 'Double_Jump.png')), (150, 20))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 12).render(str(self.player.double_jump_count), True, (255, 255, 255), (0, 0, 0)), (165, 30))         
        self.screen.blit(pg.image.load(path.join(self.item_folder, 'Sheild.png')), (200, 20))
        self.screen.blit(pg.font.Font('freesansbold.ttf', 12).render(str(self.player.bullet_shield_count), True, (255, 255, 255), (0, 0, 0)), (215, 30))
        # draws line for grappling hook
        if self.player.movingx:
            pg.draw.line(self.screen,BLUE,(self.player.pos.x,self.player.pos.y),(self.player.tempx,self.player.tempy),6)
        #pause game
        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
