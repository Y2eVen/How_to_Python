"""
Cre: Lil Hoe, Ten Fingez
"""

import pygame
from pygame.locals import *
import random

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

# fx
SLAP = "FX/Slap.mp3"
AH = "FX/Ah.mp3"

LEFT_EXHAUST = -4
RIGHT_EXHAUST = 3

pygame.init()


# define fps
FPS = 60
clock = pygame.time.Clock()


# create full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# create main surface and 2 sub surface
W, H = screen.get_size()
canvas = pygame.Surface((W, H))

rect_left = pygame.Rect(0, 0, W//2, H)
rect_right = pygame.Rect(W//2, 0, W//2, H)

sub_left = canvas.subsurface(rect_left)
sub_right = canvas.subsurface(rect_right)

# load background
background = pygame.image.load(BACKGROUND)
background = pygame.transform.scale(background, (W//2, H))


def draw_background():
    screen.blit(pygame.transform.rotate(sub_left, 180), (0, 0))
    screen.blit(sub_right, (W//2, 0))

    sub_left.blit(background, (0, 0))
    sub_right.blit(background, (0, 0))


def draw(groups):
    groups.draw(sub_left)
    groups.draw(sub_right)


# caption and icon
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(pygame.image.load(ICON))

# load sound
explosion_fx = pygame.mixer.Sound(AH)
explosion_fx.set_volume(0.25)

shoot_fx = pygame.mixer.Sound(SLAP)
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
        self.rect.center = [W//4, control * H // 8]
        self.health = 5
        self.last_shot = pygame.time.get_ticks()

        self.left_exhaust = Exhaust(self, LEFT_EXHAUST)
        self.right_exhaust = Exhaust(self, RIGHT_EXHAUST)
        exhausts.add(self.right_exhaust)
        exhausts.add(self.left_exhaust)

    def update(self):

        speed = 7
        cooldown = 500  # milliseconds
        time_now = pygame.time.get_ticks()

        pressed = pygame.key.get_pressed()

        if self.control == AROW:
            if pressed[pygame.K_UP] and self.rect.top > H//2:
                self.rect.y -= speed
            if pressed[pygame.K_DOWN] and self.rect.bottom < H:
                self.rect.y += speed
            if pressed[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if pressed[pygame.K_RIGHT] and self.rect.right < W//2:
                self.rect.x += speed

            if pressed[pygame.K_RETURN] and time_now - self.last_shot > cooldown:
                shoot_fx.play()
                bullet = Bullet(self)
                bullets.add(bullet)
                self.last_shot = time_now

            self.draw_health_bar((self.rect.bottom + 7))

        elif self.control == WASD:
            if pressed[pygame.K_w] and self.rect.bottom < H//2:
                self.rect.y += speed
            if pressed[pygame.K_s] and self.rect.top > 0:
                self.rect.y -= speed
            if pressed[pygame.K_d] and self.rect.left > 0:
                self.rect.x -= speed
            if pressed[pygame.K_a] and self.rect.right < W//2:
                self.rect.x += speed

            if pressed[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
                shoot_fx.play()
                bullet = Bullet(self)
                bullets.add(bullet)
                self.last_shot = time_now

            self.draw_health_bar((self.rect.top - 14))

    def draw_health_bar(self, y):

        def draw(surface, x, y, w, h):
            pygame.draw.rect(surface, RED, (x, y, w, h))
            t = x
            if self.health > 0:
                if self.control == WASD:
                    t += w - w * self.health//5
                pygame.draw.rect(
                    surface, GREEN, (t, y, int(w * self.health//5), h))
            else:
                explosion = Explosion(
                    self.control, self.rect.centerx, self.rect.centery, 3)
                explosions.add(explosion)
                self.left_exhaust.kill()
                self.right_exhaust.kill()
                self.kill()
            pygame.draw.rect(surface, WHITE, (x, y, w, h), 1)

        draw(sub_left, self.rect.x, y, self.rect.width, 7)
        draw(sub_right, self.rect.x, y, self.rect.width, 7)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, spacecraft):
        pygame.sprite.Sprite.__init__(self)

        self.spacecraft = spacecraft
        self.x = spacecraft.rect.centerx
        if spacecraft.control == AROW:
            self.image = pygame.image.load(PLASMA_MEDIUM)
            self.y = spacecraft.rect.top
        else:
            self.image = pygame.transform.rotate(
                pygame.image.load(LASER_MEDIUM), 180)
            self.y = spacecraft.rect.bottom

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def update(self):

        if self.spacecraft.control == AROW:
            self.rect.y -= 5
            if self.rect.bottom < 0:
                self.kill()

        else:
            self.rect.y += 5
            if self.rect.top > H:
                self.kill()

        collide = pygame.sprite.spritecollideany(
            self, spacecrafts, pygame.sprite.collide_mask)

        if collide:

            if collide != self.spacecraft:
                self.kill()
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
                img = pygame.transform.scale(img, (40, 40))
            elif size == 3:
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


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = W//2
        self.y = 0
        num = random.randint(1, 4)
        self.raw_image = pygame.image.load(
            f"PixelSpaceRage/256px/Asteroid 0{num}_png_processed.png")
        self.image = pygame.image.load(
            f"PixelSpaceRage/256px/Asteroid 0{num}_png_processed.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.speed = random.randint(2, 3)
        self.angle = 0

    def update(self):

        self.rect.y += self.speed
        self.angle += 5

        self.image = pygame.transform.rotate(self.raw_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.top > H or self.rect.bottom < 0:
            self.kill()

        collide = pygame.sprite.spritecollideany(
            self, asteroids, pygame.sprite.collide_mask)

        if collide:
            if collide != self:
                if self.speed > 1:
                    self.speed -= 1
                collide.speed += 1


time = 0


# sprite groups
spacecrafts = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
exhausts = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# create spacecrafts
red_spacecraft = Spacecraft(AROW)
blue_spacecraft = Spacecraft(WASD)

spacecrafts.add(red_spacecraft)
spacecrafts.add(blue_spacecraft)


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
    if time == 30:
        time = 0
        asteroids.add(Asteroid())

    spacecrafts.update()
    bullets.update()
    explosions.update()
    exhausts.update()
    asteroids.update()

    draw(spacecrafts)
    draw(bullets)
    draw(explosions)
    draw(exhausts)
    asteroids.draw(screen)

    pygame.display.update()

pygame.quit()
