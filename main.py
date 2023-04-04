import pygame as pg
import random
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

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.powerups.add(Grappling_Hook(70,80))
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
        for ground in GROUND:
            g = Ground(*ground)
            self.all_sprites.add(g)
            self.ground.add(g)
        for plat in PLATFORM_LIST:
            p = Platform(*plat,self)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
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
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # draws line for grappling hook
        if self.player.movingx:
            pg.draw.line(self.screen,BLUE,(self.player.pos.x,self.player.pos.y),(self.player.tempx,self.player.tempy),6)
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
