"""
Cre: Lil Hoe, Ten Fingez
"""

import pygame


CAPTION = "Game ban may bay 2 nguoi cuc manh"
ICON = "solar-system.png"
BG_IMG = "kaos-ren-space.jpg"
SC_1 = "sc_1.png"

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
pygame.display.set_caption(CAPTION)
icon = pygame.image.load(ICON)
pygame.display.set_icon(icon)

sc_1 = pygame.image.load(SC_1)

x1 = W//4 - (sc_1.get_width()//2)
y1 = 7*H//8 -(sc_1.get_height()//2)

def sc():
    sub_1.blit(sc_1,(x1, y1))
    sub_2.blit(sc_1,(x1, y1))

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

    sc()
    pygame.display.update()
