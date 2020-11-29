import pygame

pygame.init()

class SpaceCraft():
    def __init__(self, img, W, H, ctrl):
        super().__init__()

        self.W = W
        self.H = H
        self.image = img
        self.img_w = img.get_width()
        self.img_h = img.get_height()
        self.controls = ctrl
        self.x = W//4 - (self.img_w//2)
        self.y = ctrl*H//8 - (self.img_h//2)
        
    
    def draw(self, sub_1, sub_2):

        sub_1.blit(self.image,(self.x, self.y))
        sub_2.blit(self.image,(self.x, self.y))
        

    def move(self):
        pressed = pygame.key.get_pressed()

        if self.controls == 7:
            up = pressed[pygame.K_UP]
            down = pressed[pygame.K_DOWN]
            left = pressed[pygame.K_LEFT]
            right = pressed[pygame.K_RIGHT]
        elif self.controls == 1:
            up = pressed[pygame.K_s]
            down = pressed[pygame.K_w]
            left = pressed[pygame.K_d]
            right = pressed[pygame.K_a]
        
        x_diff = right - left
        y_diff = down - up
         
        self.x += x_diff * 7
        self.y += y_diff * 7
        
        x_max = self.W//2 - self.img_w
        y_max = self.H - self.img_h

        if self.x < 0:
            self.x = 0
        elif self.x > x_max:
            self.x = x_max

        if self.y < 0:
            self.y = 0
        elif self.y > y_max:
            self.y = y_max