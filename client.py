import pygame
import random
from network import Network

# define
CAPTION = "Game ban may bay 2 nguoi cuc manh"
ICON = "bullet_kin.jpg"
BACKGROUND = "PixelSpaceRage/PixelBackgroundSeamlessVertically.png"

# spacecrafts
PLAYER_RED = "PixelSpaceRage/256px/PlayerRed_Frame_01_png_processed.png"
PLAYER_BLUE = "PixelSpaceRage/256px/PlayerBlue_Frame_01_png_processed.png"

# bullets
PLASMA_MEDIUM = "PixelSpaceRage/256px/Plasma_Medium_png_processed.png"
LASER_MEDIUM = "PixelSpaceRage/256px/Laser_Medium_png_processed.png"

# controls
AROW = 7
WASD = 1

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fx
SHOOT_FX = "FX/Chius.mp3"
EXPLOSION_FX = "FX/Bumf.mp3"
THEME_FX = "FX/Review.mp3"

# bullet
TOP_BULLET = 0
LEFT_BULLET = 1
RIGHT_BULLET = -1

# exhaust
LEFT_EXHAUST = -4
RIGHT_EXHAUST = 3

pygame.init()

W = 500
H = 500

# img powerup
examplePowerup = pygame.image.load("PixelSpaceRage/256px/Powerup_Ammo_png_processed.png")
leftBoundP = examplePowerup.get_rect().w
rightBoundP = W - examplePowerup.get_rect().w

# define fps
FPS = 60
clock = pygame.time.Clock()

# create screen
screen2 = pygame.display.set_mode((W, H))

# load background
background = pygame.image.load(BACKGROUND)
background = pygame.transform.scale(background, (W, H))

# caption and icon
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(ICON))

# load sound
theme_fx = pygame.mixer.Sound(THEME_FX)
theme_fx.set_volume(0.25)
theme_fx.play(-1)

explosion_fx = pygame.mixer.Sound(EXPLOSION_FX)
explosion_fx.set_volume(0.25)

shoot_fx = pygame.mixer.Sound(SHOOT_FX)
shoot_fx.set_volume(0.25)


# spacecraft
class Spacecraft(pygame.sprite.Sprite):
    def __init__(self, control):
        pygame.sprite.Sprite.__init__(self)

        self.control = control
        if control == AROW:
            self.image = pygame.image.load(PLAYER_RED)
        else:
            self.image = pygame.transform.rotate(
                pygame.image.load(PLAYER_BLUE), 180)
        self.rect = self.image.get_rect()
        self.rect.center = [W//2, control * H // 8]
        self.health = 10
        self.max_health = 10
        self.speed = 6
        self.max_speed = 16
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 500  # milliseconds
        self.shield = 0
        self.bullets_level = 1

        self.left_exhaust = Exhaust(self, LEFT_EXHAUST)
        self.right_exhaust = Exhaust(self, RIGHT_EXHAUST)
        exhausts.add(self.right_exhaust)
        exhausts.add(self.left_exhaust)

    def update(self):

        self.move()

        self.shoot()
 
        self.health_bar()
 
        if self.shield:
            self.shield_up()

    def move(self):
        pressed = pygame.key.get_pressed()

        up = pressed[pygame.K_UP]
        down = pressed[pygame.K_DOWN]
        left = pressed[pygame.K_LEFT]
        right = pressed[pygame.K_RIGHT]
        max_top = H // 2
        max_bottom = H - 15

        if self.control == WASD:
            up = pressed[pygame.K_s]
            down = pressed[pygame.K_w]
            left = pressed[pygame.K_d]
            right = pressed[pygame.K_a]
            max_top = 15
            max_bottom = H // 2

        if up:
            self.rect.y -= self.speed
            if self.rect.top < max_top:
                self.rect.top = max_top
        if down:
            self.rect.y += self.speed
            if self.rect.bottom > max_bottom:
                self.rect.bottom = max_bottom
        if left:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if right:
            self.rect.x += self.speed
            if self.rect.right > W :
                self.rect.right = W
        
        if player == 0:
            data = n.send(f"move.{red_spacecraft.rect.center}")
            enemyPosition = eval(data)
            blue_spacecraft.moveByPos(enemyPosition)
        else:
            data = n.send(f"move.{blue_spacecraft.rect.center}")
            enemyPosition = eval(data)
            red_spacecraft.moveByPos(enemyPosition)
    
    def moveByPos(self, pos):
        self.rect.center = pos
        
    def shoot(self):
        now = pygame.time.get_ticks()
        pressed = pygame.key.get_pressed()
        pressed_key = pressed[pygame.K_RETURN]
        if self.control == WASD:
            pressed_key = pressed[pygame.K_SPACE]
        
        shootMode = 0
        if (player == 0 and self == red_spacecraft) or (player == 1 and self == blue_spacecraft):
            if pressed_key and now - self.last_shot > self.cooldown:
                shootMode = 1
                shoot_fx.play()
                if self.bullets_level == 1:
                    bullets.add(Bullet(self, TOP_BULLET))
                elif self.bullets_level == 2:
                    bullets.add(Bullet(self, LEFT_BULLET))
                    bullets.add(Bullet(self, RIGHT_BULLET))
                elif self.bullets_level == 3:
                    bullets.add(Bullet(self, TOP_BULLET))
                    bullets.add(Bullet(self, LEFT_BULLET))
                    bullets.add(Bullet(self, RIGHT_BULLET))
                self.last_shot = now
            
        
        data = n.send(f"shoot.{shootMode}")
        enemyShootMode = int(data)
        if player == 0:
            blue_spacecraft.shootByMode(enemyShootMode)
        else:
            red_spacecraft.shootByMode(enemyShootMode)
            
    def shootByMode(self, mode):
        now = pygame.time.get_ticks()
        if mode == 1 and now - self.last_shot > self.cooldown:
            shoot_fx.play()
            if self.bullets_level == 1:
                bullets.add(Bullet(self, TOP_BULLET))
            elif self.bullets_level == 2:
                bullets.add(Bullet(self, LEFT_BULLET))
                bullets.add(Bullet(self, RIGHT_BULLET))
            elif self.bullets_level == 3:
                bullets.add(Bullet(self, TOP_BULLET))
                bullets.add(Bullet(self, LEFT_BULLET))
                bullets.add(Bullet(self, RIGHT_BULLET))
            self.last_shot = now
 
    def health_bar(self):
 
        y = self.rect.bottom + 7
        if self.control == WASD:
            y = self.rect.top - 14
 
        def draw(surface, x, y, w, h):
            pygame.draw.rect(surface, RED, (x, y, w, h))
            t = x
            if self.health > 0:
                if self.control == WASD:
                    t += w - w * self.health//self.max_health
                pygame.draw.rect(
                    surface, GREEN, (t, y, int(w * self.health//self.max_health), h))
            else:
                explosion = Explosion(
                    self.control, self.rect.centerx, self.rect.centery, 2)
                explosions.add(explosion)
                self.left_exhaust.kill()
                self.right_exhaust.kill()
                self.kill()
            pygame.draw.rect(surface, WHITE, (x, y, w, h), 1)
 
        draw(screen2, self.rect.x, y, self.rect.width, 7)
 
    def shield_up(self):
 
        def draw(surface):
            surface.blit(mask_surf, (self.rect.x - 2, self.rect.y))
            surface.blit(mask_surf, (self.rect.x + 2, self.rect.y))
            surface.blit(mask_surf, (self.rect.x, self.rect.y - 2))
            surface.blit(mask_surf, (self.rect.x, self.rect.y + 2))
 
        mask = pygame.mask.from_surface(self.image)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey(BLACK)
        draw(screen2)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, spacecraft, position):
        pygame.sprite.Sprite.__init__(self)

        self.spacecraft = spacecraft
        self.position = position
        self.speed = self.spacecraft.speed

        self.x = spacecraft.rect.centerx
        if spacecraft.control == AROW:
            self.image = pygame.image.load(PLASMA_MEDIUM)
            self.y = spacecraft.rect.top
        else:
            self.image = pygame.transform.rotate(
                pygame.image.load(LASER_MEDIUM), 180)
            self.y = spacecraft.rect.bottom

        if self.position == LEFT_BULLET:
            self.image = pygame.transform.rotate(self.image, 26.5)
        elif self.position == RIGHT_BULLET:
            self.image = pygame.transform.rotate(self.image, -26.5)

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def update(self):

        if self.spacecraft.control == AROW:
            self.rect.x -= (self.position * self.speed//2)
            self.rect.y -= self.speed
        elif self.spacecraft.control == WASD:
            self.rect.x += (self.position * self.speed//2)
            self.rect.y += self.speed

        if self.rect.left < 0 or self.rect.right > W or self.rect.bottom < 0 or self.rect.top > H:
            self.kill()

        collide = pygame.sprite.spritecollideany(
            self, spacecrafts, pygame.sprite.collide_mask)
 
        if collide:
            if collide != self.spacecraft:
                self.kill()
                if collide.shield:
                    collide.shield = 0
                else:
                    collide.health -= 1
                explosion_fx.play()
                explosion = Explosion(
                    self.spacecraft.control, self.rect.centerx, self.rect.centery, 1)
                explosions.add(explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, control, x, y, size):
        pygame.sprite.Sprite.__init__(self)

        self.control = control
        self.images = []
        for num in range(1, 10):
            t = 1
            if control == WASD:
                t = 2
            img = pygame.image.load(
                f"PixelSpaceRage/256px/Explosion0{t}_Frame_0{num}_png_processed.png")
            if size == 1:
                img = pygame.transform.scale(img, (25, 25))
            elif size == 2:
                img = pygame.transform.scale(img, (160, 160))

            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3

        self.counter += 1

        if self.counter >= explosion_speed:
            if self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]
            else:
                self.kill()

class Exhaust(pygame.sprite.Sprite):
    def __init__(self, spacecraft, position):
        pygame.sprite.Sprite.__init__(self)

        self.spacecraft = spacecraft
        self.position = position
        self.x = self.spacecraft.rect.centerx
        if spacecraft.control == AROW:
            self.y = self.spacecraft.rect.bottom - 3
        else:
            self.y = self.spacecraft.rect.top + 3
        self.images = []
        for num in [1, 2, 4, 5]:
            img = pygame.image.load(
                f"PixelSpaceRage/256px/Exhaust_Frame_0{num}_png_processed.png")
            if self.spacecraft.control == WASD:
                img = pygame.transform.rotate(img, 180)
            img = pygame.transform.scale(img, (20, 20))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x + self.position, self.y]
        self.counter = 0

    def update(self):
        exhaust_speed = 4

        self.counter += 1

        if self.counter >= exhaust_speed:
            if self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]
            else:
                self.counter = 0
                self.index = 0
                self.image = self.images[self.index]

        self.x = self.spacecraft.rect.centerx
        self.y = self.spacecraft.rect.bottom - 3
        if self.spacecraft.control == WASD:
            self.y = self.spacecraft.rect.top + 3

        self.rect.center = [self.x + self.position, self.y]
        
class Powerup(pygame.sprite.Sprite):
    def __init__(self, control, choice, x):
        pygame.sprite.Sprite.__init__(self)

        self.control = control
        self.power = choice
        img = pygame.image.load(
            f"PixelSpaceRage/256px/Powerup_{self.power}_png_processed.png")
        if self.control == AROW:
            self.image = img
        elif self.control == WASD:
            self.image = pygame.transform.rotate(img, 180)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = H//2

        if self.control == AROW:
            self.rect.center = [self.x, self.y + self.rect.h//2]
        elif self.control == WASD:
            self.rect.center = [self.x, self.y - self.rect.h//2]

    def update(self):
        if self.control == AROW:
            self.rect.y += 2
        elif self.control == WASD:
            self.rect.y -= 2

        if self.rect.y < 0 or self.rect.y > H:
            self.kill()

        collide = pygame.sprite.spritecollideany(
            self, spacecrafts, pygame.sprite.collide_mask)

        if collide:

            if self.power == "Ammo":
                if collide.bullets_level < 3:
                    collide.bullets_level += 1
            elif self.power == "Energy":
                if collide.speed < collide.max_speed:
                    collide.speed += 2
            elif self.power == "Health":
                if collide.health < collide.max_health:
                    collide.health += 1
            elif self.power == "Shields":
                if not collide.shield:
                    collide.shield = 1

            self.kill()
                
def draw_background():
    screen2.blit(background, (0, 0))

# sprite groups
spacecrafts = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
exhausts = pygame.sprite.Group()
powerups = pygame.sprite.Group()


# create spacecrafts
red_spacecraft = Spacecraft(AROW)
blue_spacecraft = Spacecraft(WASD)

spacecrafts.add(red_spacecraft)
spacecrafts.add(blue_spacecraft)

n = Network()
player = n.getPlayer()

time = 0
RUNNING = True

while RUNNING:
    clock.tick(FPS)
    
    draw_background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False
                
    time += 1
    if time == 300:
        time = 0
        data = n.send(f"powerup.{leftBoundP}.{rightBoundP}")
        tokens = data.split(".")
        
        tuple1 = eval(tokens[0])
        tuple2 = eval(tokens[1])
        powerups.add(Powerup(AROW, tuple1[0], tuple1[1]))
        powerups.add(Powerup(WASD, tuple2[0], tuple2[1]))
           
    spacecrafts.update()
    bullets.update()
    explosions.update()
    exhausts.update()
    powerups.update()
    
    bullets.draw(screen2)             
    spacecrafts.draw(screen2)
    explosions.draw(screen2) 
    exhausts.draw(screen2) 
    powerups.draw(screen2) 
    
    pygame.display.update()

pygame.quit()    
