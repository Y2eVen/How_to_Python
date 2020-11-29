"""
Cre: Lil Hoe, Ten Fingez
"""

import pygame
from player import SpaceCraft


CAPTION = "Game ban may bay 2 nguoi cuc manh"
ICON = "bullet_kin.jpg"
BG_IMG = "PixelSpaceRage/PixelBackgroundSeamlessVertically.png"
SC_1 = "PixelSpaceRage/256px/PlayerRed_Frame_01_png_processed.png"
SC_2 = "PixelSpaceRage/256px/PlayerBlue_Frame_01_png_processed.png"

AROW = 7
WASD = 1

pygame.init()

# create full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# create main surface and 2 sub surface
W, H = screen.get_size()
canvas = pygame.Surface((W, H))

#print(W/2)
#print(H)

rect_1 = pygame.Rect(0,0,W//2,H)
rect_2 = pygame.Rect(W//2,0,W//2,H)

sub_1 = canvas.subsurface(rect_1)
sub_2 = canvas.subsurface(rect_2)

# background
background = pygame.image.load(BG_IMG)
background = pygame.transform.scale(background, (W//2, H))

# caption and icon
pygame.display.set_caption(CAPTION)
icon = pygame.image.load(ICON)
pygame.display.set_icon(icon)

# spacecraft
sc_1 = pygame.image.load(SC_1)
sc_2 = pygame.image.load(SC_2)

spacecraft_1 = SpaceCraft(sc_1, W, H, AROW)
spacecraft_2 = SpaceCraft(pygame.transform.rotate(sc_2, 180), W, H, WASD)

RUNNING = True
while RUNNING:

    screen.blit(pygame.transform.rotate(sub_1, 180), (0,0))
    screen.blit(sub_2, (W//2, 0))

    sub_1.blit(background, (0,0))
    sub_2.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False


    spacecraft_1.move()
    spacecraft_2.move()
    spacecraft_1.draw(sub_1, sub_2)
    spacecraft_2.draw(sub_1, sub_2)
    
    pygame.display.update()
