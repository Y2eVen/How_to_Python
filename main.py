"""
Cre: Lil Hoe, Ten Fingez
"""

import pygame


CAPTION = "Game ban may bay 2 nguoi cuc manh"
ICON = "bullet_kin.jpg"
BG_IMG = "PixelBackgroundSeamlessVertically.png"
SC_1 = "PlayerRed_Frame_01_png_processed.png"

pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = screen.get_size()
canvas = pygame.Surface((W, H))

print(W/2)
print(H)

rect_1 = pygame.Rect(0,0,W//2,H)
rect_2 = pygame.Rect(W//2,0,W//2,H)

sub_1 = canvas.subsurface(rect_1)
sub_2 = canvas.subsurface(rect_2)


background = pygame.image.load(BG_IMG)
background = pygame.transform.scale(background, (W//2, H))
pygame.display.set_caption(CAPTION)
icon = pygame.image.load(ICON)
pygame.display.set_icon(icon)

sc_1 = pygame.image.load(SC_1)

def sc(c):
    w = c.get_width()
    h = c.get_height()
    x = W//4 - (w//2)
    y = 7*H//8 -(h//2)
    sub_1.blit(c,(x, y))
    sub_2.blit(c,(x, y))

RUNNING = True
while RUNNING:

    screen.blit(sub_1, (0,0))
    screen.blit(sub_2, (W//2, 0))

    sub_1.blit(background, (0,0))
    sub_2.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False

    sc(sc_1)
    pygame.display.update()
