import random

# game options/settings
TITLE = "Bullet Bounce"
WIDTH = 480
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8

# Starting platforms
    #Shotgun Level
SGPLATFORM_LIST = [(WIDTH, HEIGHT-80, 60, 20),
                 (WIDTH, (HEIGHT*3/4)-70, 60, 20),
                 (WIDTH, (HEIGHT/2)-60, 60, 20),
                 (WIDTH, (HEIGHT/4)-50, 60, 20),
##                   (WIDTH + 150, HEIGHT-50, 60, 20),
##                 (WIDTH + 150, (HEIGHT*3/4)-50, 60, 20),
##                 (WIDTH + 150, (HEIGHT/2)-40, 60, 20),
##                 (WIDTH + 150, (HEIGHT/4)-50, 60, 20),
                 (WIDTH+200, HEIGHT-80, 60, 20),
                 (WIDTH+200, (HEIGHT*3/4)-70, 60, 20),
                 (WIDTH+200, (HEIGHT/2)-60, 60, 20),
                 (WIDTH+200, (HEIGHT/4)-50, 60, 20)]
    #Machine Gun Level
MGPLATFORM_LIST = [((random.randrange(WIDTH, WIDTH + 200)), HEIGHT-80, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)), (HEIGHT*3/4)-70, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)), (HEIGHT/2)-60, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)), (HEIGHT/4)-50, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)+300), HEIGHT-80, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)+300), (HEIGHT*3/4)-70, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)+300), (HEIGHT/2)-60, 150, 20),
                 ((random.randrange(WIDTH, WIDTH + 200)+300), (HEIGHT/4)-50, 150, 20)]

# Ground
GROUND = [(0, HEIGHT - 40, WIDTH, 40)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)

#Definitions for Grappling hook
RANGE = 250
DISTFROMBOTPLAT = 60
SPEEDMULT = 0.07

#Items
ITEM_IMAGE = {"Grappling_Hook": 'Grappling_Hook.png', "Double_Jump": 'Double_Jump.png', "Bullet_Shield": 'Sheild.png', "Health": 'Heart.png'}
BOB_RANGE = 2
BOB_SPEED = 0.1

#Sounds
EFFECT_SOUNDS = {'Grappling_Hook': 'Grappling_Hook_Powerup.wav','Double_Jump': 'Jump.wav', 'Bullet_Shield': 'Bullet_Shield.wav', 'Health': 'Health.wav', 'Damage': 'Damage.wav', 'Death': 'Death.wav'}
