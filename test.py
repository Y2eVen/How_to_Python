import pygame as pg
import numpy as np
 
'''
simple splitscreen example
 
move the Green player with the arrow keys
and the red player with WASD.
 
'''
 
 
# constants for the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
 
# constants for the different control schemes
ARROW = 0
WASD = 1
 
# setup the display
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
 
# define the canvas as a suface for the whole screen
canvas = pg.Surface((screen_width, screen_height))
 
# define two rects with the size half of the canvas
p1_camera = pg.Rect(0, 0, screen_width // 2, screen_height)
p2_camera = pg.Rect(screen_width // 2, 0, screen_width// 2, screen_height)
 
# draw a background
#background = pg.Surface((screen_width // 2, screen_height))
#background.fill(BLUE)
background = pg.image.load("kaos-ren-space.jpg")
 
sub1 = canvas.subsurface(p1_camera)
sub2 = canvas.subsurface(p2_camera)
 
 
class Player(pg.sprite.Sprite):
    def __init__(self, pos, color, controls):
        super().__init__()
        self.dir = np.array([0, 0])
        self.vel = 5 
        self.bb_width, self.bb_height = 56, 56
        self.rect = pg.Rect(pos, (self.bb_width, self.bb_height))
 
        self.color = color
        self.image = pg.Surface([self.bb_width, self.bb_height])
        self.image.fill(self.color)
        self.controls = controls
    
    def update(self):
        pressed = pg.key.get_pressed()
        if self.controls == ARROW:
            move_up = pressed[pg.K_UP]
            move_down = pressed[pg.K_DOWN]
            move_left = pressed[pg.K_LEFT]
            move_right = pressed[pg.K_RIGHT]
        elif self.controls == WASD:
            move_up = pressed[pg.K_w]
            move_down = pressed[pg.K_s]
            move_left = pressed[pg.K_a]
            move_right = pressed[pg.K_d]
        # calculate direction based on the inputs
        self.dir = np.array([move_right - move_left, move_down - move_up])
        # set new position based on adding the directional vector * the velocity
        self.rect.topleft = np.add(self.rect.topleft, self.dir * self.vel)
        
players = pg.sprite.Group()
player1 = Player((20, 20), GREEN, ARROW)
player2 = Player((120, 60), RED, WASD)
players.add(player1)
players.add(player2)
 
pg.init()
clock = pg.time.Clock()
 
running = True
while running:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    #update the game logic
    players.update()
    
    # blit the subscreens
    screen.blit(sub1, (0, 0))
    screen.blit(pg.transform.rotate(sub2, 180), (screen_width // 2, 0))
    #blit the background image
    sub1.blit(background, (0, 0))
    sub2.blit(background, (0, 0))
    # draw lines that seperate the screens
    pg.draw.line(sub1, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)
    pg.draw.line(sub2, WHITE, (0, 0), (0, screen_height), 5)
    # draw the player objects on each of the subscreens
    players.draw(sub1)
    players.draw(sub2)
            
    pg.display.update()
    clock.tick(60)
    
pg.quit()