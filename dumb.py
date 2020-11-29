import pygame

pygame.init()

class SpaceCraft():
    def __init__(self, x, y, ctrl):
        super().__init__()

        
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.controls = ctrl
               
    def move(self):
        pressed = pygame.key.get_pressed()

        if self.controls == 7:
            up = pressed[pygame.K_UP]
            down = pressed[pygame.K_DOWN]
            left = pressed[pygame.K_LEFT]
            right = pressed[pygame.K_RIGHT]
        elif self.controls == 1:
            up = pressed[pygame.K_w]
            down = pressed[pygame.K_s]
            left = pressed[pygame.K_a]
            right = pressed[pygame.K_d]
        
        self.x += (right - left)*0.5
        self.y += (down - up)*0.5
        
    def pr(self):
        print(self.x)
        print(self.y)
        print(self.position)


test = SpaceCraft(5, 6, 7)
while True:

    test.move()
    test.pr()
    pygame.time.delay(5000)
