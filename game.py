"""
Cre: Lil Hoe, Ten Fingez
"""

import pygame
from pygame.locals import *
import random
import math
from network import Network

from menu import *

class Game:

    pygame.init()

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
    AROW = 1
    WASD = -1

    # colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 204, 0)

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

    # fps
    clock = pygame.time.Clock()
    FPS = 30

    # create full window
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    WIDTH = window.get_width()
    HEIGHT = window.get_height()

    # create main surface and 2 sub surface
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvaz = pygame.Surface((WIDTH, HEIGHT))

    left_rect = pygame.Rect(0, 0, WIDTH//2, HEIGHT)
    right_rect = pygame.Rect(WIDTH//2, 0, WIDTH//2, HEIGHT)
    left_sub = canvas.subsurface(left_rect)
    right_sub = canvas.subsurface(right_rect)

    # create client's surface 
    canvas = pygame.Surface((2*WIDTH, 2*HEIGHT))
    screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    clientScreen = canvas.subsurface(screen_rect)
    
    # load background
    background = pygame.transform.scale(
        pygame.image.load(BACKGROUND), (WIDTH//2, HEIGHT))
    
    # load client's background
    clientBackground = pygame.transform.scale(pygame.image.load(BACKGROUND), (WIDTH, HEIGHT))

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

    # sprite groups
    spacecrafts = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    exhausts = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    def __init__(self):
        self.RUNNING = True
        self.PLAYING = False
        self.CLIENT = False
        self.UP_KEY, self.DOWN_KEY, self.SELECT_KEY, self.BACK_KEY = False, False, False, False
        self.time = 0
        self.font_name = 'editundo.ttf'
        self.main_menu = MainMenu(self)
        self.start = StartMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.menu = self.main_menu
        
        # bound of powerup spawn
        examplePowerup = pygame.image.load("PixelSpaceRage/256px/Powerup_Ammo_png_processed.png")
        self.leftBoundP = examplePowerup.get_rect().w*3//2
        self.rightBoundP = self.WIDTH - examplePowerup.get_rect().w*3//2

    def loop(self):

        if self.PLAYING:
            self.create_spacecrafts()
        if self.CLIENT:
            self.create_client_spacecrafts()
        
        while self.PLAYING:
            
            self.draw_background()

            self.check_events()

            self.drop()

            self.spacecrafts.update()
            self.bullets.update()
            self.explosions.update()
            self.exhausts.update()
            self.powerups.update()
            self.asteroids.update()

            self.draw_group(self.spacecrafts)
            self.draw_group(self.bullets)
            self.draw_group(self.explosions)
            self.draw_group(self.exhausts)
            self.draw_group(self.powerups)
            self.asteroids.draw(self.window)

            pygame.display.update()
            self.clock.tick(self.FPS)
            
        while self.CLIENT:
            self.clock.tick(self.FPS)
    
            self.draw_client_background()
            
            self.check_events()    
            
            self.waitting = int(self.netWork.send("waitting."))
            if self.waitting:       
                self.showWaittingText()
            else:           
                self.time += 1
                if self.time == 300:
                    self.time = 0
                    data = self.netWork.send(f"powerup.{self.leftBoundP}.{self.rightBoundP}")
                    tokens = data.split(".")
                      
                    tuple1 = eval(tokens[0])
                    tuple2 = eval(tokens[1])
                    self.powerups.add(ClientPowerup(self.AROW, tuple1[0], tuple1[1], self))
                    self.powerups.add(ClientPowerup(self.WASD, tuple2[0], tuple2[1], self))
                         
                self.spacecrafts.update()
                self.bullets.update()
                self.explosions.update()
                self.exhausts.update()
                self.powerups.update()
                  
                self.bullets.draw(self.clientScreen)             
                self.spacecrafts.draw(self.clientScreen)
                self.explosions.draw(self.clientScreen) 
                self.exhausts.draw(self.clientScreen) 
                self.powerups.draw(self.clientScreen) 
             
            pygame.display.update()

    def create_spacecrafts(self):
        # create spacecrafts
        red_spacecraft = Spacecraft(self.AROW, self)
        blue_spacecraft = Spacecraft(self.WASD, self)

        self.spacecrafts.add(red_spacecraft)
        self.spacecrafts.add(blue_spacecraft)
        
    def create_client_spacecrafts(self):
        # create spacecrafts
        self.red_spacecraft = ClientSpacecraft(self.AROW, self)
        self.blue_spacecraft = ClientSpacecraft(self.WASD, self)

        self.spacecrafts.add(self.red_spacecraft)
        self.spacecrafts.add(self.blue_spacecraft)

    def draw_background(self):

        self.window.blit(pygame.transform.rotate(self.left_sub, 180), (0, 0))
        self.window.blit(self.right_sub, (self.WIDTH // 2, 0))

        self.left_sub.blit(self.background, (0, 0))
        self.right_sub.blit(self.background, (0, 0))
        
    def draw_client_background(self):
        if self.player == 0:
            self.window.blit(self.clientScreen, (0, 0))
        else:
            self.window.blit(pygame.transform.rotate(self.clientScreen, 180), (0, 0))
        self.clientScreen.blit(self.clientBackground, (0, 0))
    
    def showWaittingText(self):
        text = "Waitting for another player ..."
        font = pygame.font.Font(self.font_name, 32)
        textWidth, textHeight = font.size(text)
        waittingText = font.render(text, True, self.YELLOW)
        self.window.blit(waittingText, (self.WIDTH//2 - textWidth//2, self.HEIGHT//2 - textHeight//2))

    def draw_group(self, groups):
        groups.draw(self.left_sub)
        groups.draw(self.right_sub)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.PLAYING = False
                self.RUNNING = False
                self.CLIENT = False
                self.menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.PLAYING = False
                    self.RUNNING = False
                    self.CLIENT = False
                    self.menu.run_display = False
                if event.key == pygame.K_RETURN:
                    self.SELECT_KEY = True
                if event.key == pygame.K_SPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.SELECT_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvaz.blit(text_surface, text_rect)

    def drop(self):
        self.time += 1
        if self.time % 30 == 0:
            self.asteroids.add(Asteroid())

        if self.time == 300:
            self.time = 0
            self.powerups.add(Powerup(self.AROW))
            self.powerups.add(Powerup(self.WASD))


class Spacecraft(pygame.sprite.Sprite):
    def __init__(self, control, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.control = control
        if control == Game.AROW:
            self.image = pygame.image.load(Game.PLAYER_RED)
        else:
            self.image = pygame.transform.rotate(
                pygame.image.load(Game.PLAYER_BLUE), 180)
        self.rect = self.image.get_rect()
        self.rect.center = [Game.WIDTH//4,
                            (4 + control * 3) * Game.HEIGHT // 8]
        self.health = 10
        self.max_health = 10
        self.speed = 6
        self.max_speed = 16
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 500  # milliseconds
        self.shield = 0
        self.bullets_level = 1

        self.left_exhaust = Exhaust(self, Game.LEFT_EXHAUST)
        self.right_exhaust = Exhaust(self, Game.RIGHT_EXHAUST)
        Game.exhausts.add(self.right_exhaust)
        Game.exhausts.add(self.left_exhaust)

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
        max_top = Game.HEIGHT // 2
        max_bottom = Game.HEIGHT - 15

        if self.control == Game.WASD:
            up = pressed[pygame.K_s]
            down = pressed[pygame.K_w]
            left = pressed[pygame.K_d]
            right = pressed[pygame.K_a]
            max_top = 15
            max_bottom = Game.HEIGHT // 2

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
            if self.rect.right > Game.WIDTH // 2:
                self.rect.right = Game.WIDTH//2

    def shoot(self):
        now = pygame.time.get_ticks()
        pressed = pygame.key.get_pressed()
        pressed_key = pressed[pygame.K_RETURN]
        if self.control == Game.WASD:
            pressed_key = pressed[pygame.K_SPACE]

        if pressed_key and now - self.last_shot > self.cooldown:
            Game.shoot_fx.play()
            if self.bullets_level == 1:
                Game.bullets.add(Bullet(self, Game.TOP_BULLET, self.game))
            elif self.bullets_level == 2:
                Game.bullets.add(Bullet(self, Game.LEFT_BULLET, self.game))
                Game.bullets.add(Bullet(self, Game.RIGHT_BULLET, self.game))
            elif self.bullets_level == 3:
                Game.bullets.add(Bullet(self, Game.TOP_BULLET, self.game))
                Game.bullets.add(Bullet(self, Game.LEFT_BULLET, self.game))
                Game.bullets.add(Bullet(self, Game.RIGHT_BULLET, self.game))
            self.last_shot = now

    def health_bar(self):

        y = self.rect.bottom + 7
        if self.control == Game.WASD:
            y = self.rect.top - 14

        def draw(surface, x, y, w, h):
            pygame.draw.rect(surface, Game.RED, (x, y, w, h))
            t = x
            if self.health > 0:
                if self.control == Game.WASD:
                    t += w - w * self.health//self.max_health
                pygame.draw.rect(
                    surface, Game.GREEN, (t, y, int(w * self.health//self.max_health), h))
            else:
                explosion = Explosion(
                    self.control, self.rect.centerx, self.rect.centery, 2)
                Game.explosions.add(explosion)
                self.left_exhaust.kill()
                self.right_exhaust.kill()
                self.kill()
            pygame.draw.rect(surface, Game.WHITE, (x, y, w, h), 1)

        draw(Game.left_sub, self.rect.x, y, self.rect.width, 7)
        draw(Game.right_sub, self.rect.x, y, self.rect.width, 7)

    def shield_up(self):

        def draw(surface):
            surface.blit(mask_surf, (self.rect.x - 2, self.rect.y))
            surface.blit(mask_surf, (self.rect.x + 2, self.rect.y))
            surface.blit(mask_surf, (self.rect.x, self.rect.y - 2))
            surface.blit(mask_surf, (self.rect.x, self.rect.y + 2))

        mask = pygame.mask.from_surface(self.image)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey(Game.BLACK)
        draw(Game.right_sub)
        draw(Game.left_sub)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, spacecraft, position, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.spacecraft = spacecraft
        self.position = position
        self.speed = self.spacecraft.speed

        self.x = spacecraft.rect.centerx
        if spacecraft.control == Game.AROW:
            self.image = pygame.image.load(Game.PLASMA_MEDIUM)
            self.y = spacecraft.rect.top
        else:
            self.image = pygame.transform.rotate(
                pygame.image.load(Game.LASER_MEDIUM), 180)
            self.y = spacecraft.rect.bottom

        if self.position == Game.LEFT_BULLET:
            self.image = pygame.transform.rotate(self.image, 26.5)
        elif self.position == Game.RIGHT_BULLET:
            self.image = pygame.transform.rotate(self.image, -26.5)

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def update(self):

        self.rect.x -= self.spacecraft.control * self.position * self.speed//2
        self.rect.y -= self.spacecraft.control * self.speed

        if self.game.PLAYING:
            if (self.rect.left < 0 or self.rect.right > Game.WIDTH // 2 or self.rect.bottom < 0 or self.rect.top > Game.HEIGHT):
                self.kill()
        elif self.game.CLIENT: 
            if (self.rect.left < 0 or self.rect.right > Game.WIDTH or self.rect.bottom < 0 or self.rect.top > Game.HEIGHT):
                self.kill()
        collide = pygame.sprite.spritecollideany(
            self, Game.spacecrafts, pygame.sprite.collide_mask)

        if collide:
            if collide != self.spacecraft:
                self.kill()
                if collide.shield:
                    collide.shield = 0
                else:
                    collide.health -= 1
                Game.explosion_fx.play()
                explosion = Explosion(
                    self.spacecraft.control, self.rect.centerx, self.rect.centery, 1)
                Game.explosions.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, control, x, y, size):
        pygame.sprite.Sprite.__init__(self)

        self.control = control
        self.images = []
        for num in range(1, 10):
            exp = int(1 + (1/2 * (1 - self.control)))
            img = pygame.image.load(
                f"PixelSpaceRage/256px/Explosion0{exp}_Frame_0{num}_png_processed.png")
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
        self.y = self.spacecraft.rect.bottom - 3
        if spacecraft.control == Game.WASD:
            self.y = self.spacecraft.rect.top + 3
        self.images = []
        for num in [1, 2, 4, 5]:
            img = pygame.image.load(
                f"PixelSpaceRage/256px/Exhaust_Frame_0{num}_png_processed.png")
            if self.spacecraft.control == Game.WASD:
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
        if self.spacecraft.control == Game.WASD:
            self.y = self.spacecraft.rect.top + 3

        self.rect.center = [self.x + self.position, self.y]


class Powerup(pygame.sprite.Sprite):
    def __init__(self, control):
        pygame.sprite.Sprite.__init__(self)

        self.control = control
        self.power = random.choice(["Ammo", "Energy", "Health", "Shields"])
        img = pygame.image.load(
            f"PixelSpaceRage/256px/Powerup_{self.power}_png_processed.png")
        if self.control == Game.WASD:
            img = pygame.transform.rotate(img, 180)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = random.randint(self.rect.w, Game.WIDTH//2 - self.rect.w)
        self.y = Game.HEIGHT//2

        self.rect.center = [self.x, self.y + self.control * self.rect.h//2]

        self.speed = 5

    def update(self):

        self.rect.y += self.control * self.speed

        if self.rect.y < 0 or self.rect.y > Game.HEIGHT:
            self.kill()

        collide = pygame.sprite.spritecollideany(
            self, Game.spacecrafts, pygame.sprite.collide_mask)

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


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = Game.WIDTH//2
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
        self.angle += self.speed

        self.image = pygame.transform.rotate(self.raw_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.top > Game.HEIGHT or self.rect.bottom < 0:
            self.kill()

        collide = pygame.sprite.spritecollideany(
            self, Game.asteroids, pygame.sprite.collide_mask)

        if collide:
            if collide != self:
                if self.speed > 1:
                    self.speed -= 1
                collide.speed += 1
                
class ClientPowerup(pygame.sprite.Sprite):
    def __init__(self, control, choice, x, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.control = control
        self.power = choice
        img = pygame.image.load(f"PixelSpaceRage/256px/Powerup_{self.power}_png_processed.png")
        if self.control == Game.AROW:
            self.image = img
        elif self.control == Game.WASD:
            self.image = pygame.transform.rotate(img, 180)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = Game.HEIGHT//2

        self.rect.center = [self.x, self.y + self.control * self.rect.h//2]

        self.speed = 5

    def update(self):
        self.rect.y += self.control * self.speed

        if self.rect.y < 0 or self.rect.y > Game.HEIGHT:
            self.kill()

        collide = pygame.sprite.spritecollideany(
            self, self.game.spacecrafts, pygame.sprite.collide_mask)

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
            
class ClientSpacecraft(pygame.sprite.Sprite):
    def __init__(self, control, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.control = control
        if control == Game.AROW:
            self.image = pygame.image.load(Game.PLAYER_RED)
        else:
            self.image = pygame.transform.rotate(
                pygame.image.load(Game.PLAYER_BLUE), 180)
        self.rect = self.image.get_rect()
        self.rect.center = [Game.WIDTH//2, (4 + control * 3) * Game.HEIGHT // 8]
        self.health = 10
        self.max_health = 10
        self.speed = 6
        self.max_speed = 16
        self.last_shot = pygame.time.get_ticks()
        self.cooldown = 500  # milliseconds
        self.shield = 0
        self.bullets_level = 1

        self.left_exhaust = Exhaust(self, Game.LEFT_EXHAUST)
        self.right_exhaust = Exhaust(self, Game.RIGHT_EXHAUST)
        self.game.exhausts.add(self.right_exhaust)
        self.game.exhausts.add(self.left_exhaust)
        
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
        max_top = Game.HEIGHT // 2
        max_bottom = Game.HEIGHT - 15

        if self.control == Game.WASD:
            up = pressed[pygame.K_s]
            down = pressed[pygame.K_w]
            left = pressed[pygame.K_d]
            right = pressed[pygame.K_a]
            max_top = 15
            max_bottom = Game.HEIGHT // 2

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
            if self.rect.right > Game.WIDTH :
                self.rect.right = Game.WIDTH
        
        if self.game.player == 0:
            data = self.game.netWork.send(f"move.{self.game.red_spacecraft.rect.center}")
            enemyPosition = eval(data)
            self.game.blue_spacecraft.moveByPos(enemyPosition)
        else:
            data = self.game.netWork.send(f"move.{self.game.blue_spacecraft.rect.center}")
            enemyPosition = eval(data)
            self.game.red_spacecraft.moveByPos(enemyPosition)
    
    def moveByPos(self, pos):
        self.rect.center = pos
        
    def shoot(self):
        now = pygame.time.get_ticks()
        pressed = pygame.key.get_pressed()
        pressed_key = pressed[pygame.K_RETURN]
        if self.control == Game.WASD:
            pressed_key = pressed[pygame.K_SPACE]
        
        shootMode = 0
        if (self.game.player == 0 and self == self.game.red_spacecraft) or (self.game.player == 1 and self == self.game.blue_spacecraft):
            if pressed_key and now - self.last_shot > self.cooldown:
                shootMode = 1
                self.game.shoot_fx.play()
                if self.bullets_level == 1:
                    self.game.bullets.add(Bullet(self, Game.TOP_BULLET, self.game))
                elif self.bullets_level == 2:
                    self.game.bullets.add(Bullet(self, Game.LEFT_BULLET, self.game))
                    self.game.bullets.add(Bullet(self, Game.RIGHT_BULLET, self.game))
                elif self.bullets_level == 3:
                    self.game.bullets.add(Bullet(self, Game.TOP_BULLET, self.game))
                    self.game.bullets.add(Bullet(self, Game.LEFT_BULLET, self.game))
                    self.game.bullets.add(Bullet(self, Game.RIGHT_BULLET, self.game))
                self.last_shot = now
            
        
        data = self.game.netWork.send(f"shoot.{shootMode}")
        enemyShootMode = int(data)
        if self.game.player == 0:
            self.game.blue_spacecraft.shootByMode(enemyShootMode)
        else:
            self.game.red_spacecraft.shootByMode(enemyShootMode)
            
    def shootByMode(self, mode):
        now = pygame.time.get_ticks()
        if mode == 1 and now - self.last_shot > self.cooldown:
            self.game.shoot_fx.play()
            if self.bullets_level == 1:
                self.game.bullets.add(Bullet(self, Game.TOP_BULLET, self.game))
            elif self.bullets_level == 2:
                self.game.bullets.add(Bullet(self, Game.LEFT_BULLET, self.game))
                self.game.bullets.add(Bullet(self, Game.RIGHT_BULLET, self.game))
            elif self.bullets_level == 3:
                self.game.bullets.add(Bullet(self, Game.TOP_BULLET, self.game))
                self.game.bullets.add(Bullet(self, Game.LEFT_BULLET, self.game))
                self.game.bullets.add(Bullet(self, Game.RIGHT_BULLET, self.game))
            self.last_shot = now
 
    def health_bar(self):
        y = self.rect.bottom + 7
        if self.control == self.game.WASD:
            y = self.rect.top - 14
 
        def draw(surface, x, y, w, h):
            pygame.draw.rect(surface, self.game.RED, (x, y, w, h))
            t = x
            if self.health > 0:
                if self.control == self.game.WASD:
                    t += w - w * self.health//self.max_health
                pygame.draw.rect(
                    surface, self.game.GREEN, (t, y, int(w * self.health//self.max_health), h))
            else:
                explosion = Explosion(
                    self.control, self.rect.centerx, self.rect.centery, 2)
                self.game.explosions.add(explosion)
                self.left_exhaust.kill()
                self.right_exhaust.kill()
                self.kill()
            pygame.draw.rect(surface, self.game.WHITE, (x, y, w, h), 1)
 
        draw(self.game.clientScreen, self.rect.x, y, self.rect.width, 7)
 
    def shield_up(self):
        def draw(surface):
            surface.blit(mask_surf, (self.rect.x - 2, self.rect.y))
            surface.blit(mask_surf, (self.rect.x + 2, self.rect.y))
            surface.blit(mask_surf, (self.rect.x, self.rect.y - 2))
            surface.blit(mask_surf, (self.rect.x, self.rect.y + 2))
 
        mask = pygame.mask.from_surface(self.image)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey(self.game.BLACK)
        draw(self.game.clientScreen)
