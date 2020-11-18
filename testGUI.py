'''
Created on Nov 17, 2020

@author: lenovo
'''
import pygame

pygame.init()

flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((640, 480))


GREY = (150,150,150)

running = True

while running:
    screen.fill(GREY)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    
pygame.quit()    