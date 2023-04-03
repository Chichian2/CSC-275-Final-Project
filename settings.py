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
#PLATFORM_LIST = [(WIDTH, HEIGHT-80, 150, 20),
#                 (WIDTH, (HEIGHT*3/4)-70, 150, 20),
#                 (WIDTH, (HEIGHT/2)-60, 150, 20),
#                 (WIDTH, (HEIGHT/4)-50, 150, 20),
#                 (WIDTH+300, HEIGHT-80, 150, 20),
#                 (WIDTH+300, (HEIGHT*3/4)-70, 150, 20),
#                 (WIDTH+300, (HEIGHT/2)-60, 150, 20),
#                 (WIDTH+300, (HEIGHT/4)-50, 150, 20)]
    #Machine Gun Level
PLATFORM_LIST = [((random.randrange(WIDTH, WIDTH + 200)), HEIGHT-80, 150, 20),
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
