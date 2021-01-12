import pygame
from network import Network


class Menu():
    def __init__(self, game):

        self.game = game
        self.font_size = 50
        self.mid_w, self.mid_h = self.game.WIDTH // 2, self.game.HEIGHT // 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(
            0, 0, self.font_size + 5, self.font_size + 5)
        self.offset = - self.font_size * 5

    def draw_cursor(self):
        self.game.draw_text('>', self.font_size,
                            self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.canvaz, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + self.font_size + 10
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + self.font_size * 2 + 10
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + self.font_size * 3 + 10
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:

            self.game.check_events()
            self.check_input()
            self.game.canvaz.fill(self.game.BLACK)
            self.game.draw_text(
                'Game Ban May Bay 2 Nguoi', self.font_size, self.game.WIDTH // 2, self.game.HEIGHT // 2 - self.font_size)
            self.game.draw_text("Start Game", self.font_size,
                                self.startx, self.starty)
            self.game.draw_text("Options", self.font_size,
                                self.optionsx, self.optionsy)
            self.game.draw_text("Credits", self.font_size,
                                self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.SELECT_KEY:
            if self.state == 'Start':

                self.game.menu = self.game.start
            elif self.state == 'Options':
                self.game.menu = self.game.options
            elif self.state == 'Credits':
                self.game.menu = self.game.credits
            self.run_display = False


class StartMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Tandem'
        self.tandemx, self.tandemy = self.mid_w, self.mid_h + self.font_size
        self.lclx, self.lcly = self.mid_w, self.mid_h + self.font_size * 2
        self.botx, self.boty = self.mid_w, self.mid_h + self.font_size * 3
        self.cursor_rect.midtop = (self.tandemx + self.offset, self.tandemy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.canvaz.fill((0, 0, 0))
            self.game.draw_text(
                'Game Mode', self.font_size, self.game.WIDTH / 2, self.game.HEIGHT / 2 - (self.font_size + 10))
            self.game.draw_text("Tandem", self.font_size,
                                self.tandemx, self.tandemy)
            self.game.draw_text("Local", self.font_size, self.lclx, self.lcly)
            self.game.draw_text("Bot", self.font_size, self.botx, self.boty)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Tandem':
                self.cursor_rect.midtop = (
                    self.lclx + self.offset, self.lcly)
                self.state = 'Local'
            elif self.state == 'Local':
                self.cursor_rect.midtop = (
                    self.botx + self.offset, self.boty)
                self.state = 'Bot'
            elif self.state == 'Bot':
                self.cursor_rect.midtop = (
                    self.tandemx + self.offset, self.tandemy)
                self.state = 'Tandem'
        elif self.game.UP_KEY:
            if self.state == 'Tandem':
                self.cursor_rect.midtop = (
                    self.botx + self.offset, self.boty)
                self.state = 'Bot'
            elif self.state == 'Local':
                self.cursor_rect.midtop = (
                    self.tandemx + self.offset, self.tandemy)
                self.state = 'Tandem'
            elif self.state == 'Bot':
                self.cursor_rect.midtop = (
                    self.lclx + self.offset, self.lcly)
                self.state = 'Local'

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.menu = self.game.main_menu
            self.run_display = False
        elif self.game.SELECT_KEY:
            if self.state == 'Tandem':
                self.game.PLAYING = True

            elif self.state == 'Local':
                self.game.CLIENT = True
                self.game.netWork = Network()
                self.game.player = self.game.netWork.getPlayer()
                self.game.waitting = 0
            elif self.state == 'Bot':
                pass
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + self.font_size
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + self.font_size * 2
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.canvaz.fill((0, 0, 0))
            self.game.draw_text(
                'Options', self.font_size, self.game.WIDTH / 2, self.game.HEIGHT / 2 - (self.font_size + 10))
            self.game.draw_text("Volume", self.font_size -
                                10, self.volx, self.voly)
            self.game.draw_text("Controls", self.font_size -
                                10, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.SELECT_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.SELECT_KEY or self.game.BACK_KEY:
                self.game.menu = self.game.main_menu
                self.run_display = False
            self.game.canvaz.fill(self.game.BLACK)
            self.game.draw_text(
                'Credits', self.font_size, self.game.WIDTH // 2, self.game.HEIGHT // 2 - self.font_size)
            self.game.draw_text(
                'Made by Lil Hoe & Ten Fingez', self.font_size - 10, self.game.WIDTH / 2, self.game.HEIGHT / 2 + self.font_size//2)
            self.blit_screen()


class PausedMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'New'
        self.newx, self.newy = self.mid_w, self.mid_h + self.font_size
        self.menux, self.menuy = self.mid_w, self.mid_h + self.font_size * 2
        self.cursor_rect.midtop = (self.newx + self.offset, self.newy)

    def display_menu(self):

        self.game.check_events()
        self.check_input()
        self.game.canvaz.fill((0, 0, 0))

        self.game.draw_text(
            'Paused', self.font_size, self.game.WIDTH / 2, self.game.HEIGHT / 2 - (self.font_size + 10))
        self.game.draw_text("New Game", self.font_size -
                            10, self.newx, self.newy)
        self.game.draw_text("Main Menu", self.font_size -
                            10, self.menux, self.menuy)
        self.draw_cursor()
        self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            pass
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'New':
                self.state = 'Menu'
                self.cursor_rect.midtop = (
                    self.menux + self.offset, self.menuy)
            elif self.state == 'Menu':
                self.state = 'New'
                self.cursor_rect.midtop = (self.newx + self.offset, self.newy)
        elif self.game.SELECT_KEY:
            if self.state == 'New':
                self.game.reset_game()
                self.game.create_spacecrafts()
                self.game.paused = False
            elif self.state == 'Menu':
                self.game.PLAYING = False
                self.game.paused = False
                self.game.reset_game()
                self.game.menu = self.game.main_menu


class GameoverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'New'
        self.newx, self.newy = self.mid_w, self.mid_h + self.font_size
        self.menux, self.menuy = self.mid_w, self.mid_h + self.font_size * 2
        self.cursor_rect.midtop = (self.newx + self.offset, self.newy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.canvaz.fill((0, 0, 0))

            self.game.draw_text(
                'Game over', self.font_size, self.game.WIDTH / 2, self.game.HEIGHT / 2 - (self.font_size + 10))
            self.game.draw_text("New Game", self.font_size -
                                10, self.newx, self.newy)
            self.game.draw_text("Main Menu", self.font_size -
                                10, self.menux, self.menuy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            pass
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'New':
                self.state = 'Menu'
                self.cursor_rect.midtop = (
                    self.menux + self.offset, self.menuy)
            elif self.state == 'Menu':
                self.state = 'New'
                self.cursor_rect.midtop = (self.newx + self.offset, self.newy)
        elif self.game.SELECT_KEY:
            if self.state == 'New':
                self.game.PLAYING = True

            elif self.state == 'Menu':
                self.game.menu = self.game.main_menu
            self.run_display = False
