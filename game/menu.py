import pygame as pg
import sys
from .utils import *
# from .settings import WINDOW_SIZE



class StartMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()

        self.logo = pg.transform.scale(pg.image.load('assets/images/ui/Logo.png').convert_alpha(), (900, 390))

        self.background_images = []  # List of background images (since they are setup for paralax)
        self.load_background('forest_4', 7)

        self.mouse_rect = None

        self.button_rects = []
        self.load_buttons()

    def load_background(self, name: str, qty: int):
        path = 'assets/images/backgrounds/' + name + '/'
        for i in range (1, qty + 1):
            image = pg.image.load(path + str(i) + '.png')
            self.background_images.append(image)

    def load_buttons(self):
        play_button = pg.Rect(self.screen_size[0] / 2 - 138, (self.screen_size[1] / 2 - self.logo.get_height() / 2) + 232, 260, 100)
        self.button_rects.append(play_button)

        load_button = pg.Rect(self.screen_size[0] / 2 - 400, (self.screen_size[1] / 2 - self.logo.get_height() / 2) + 232, 130, 100)
        self.button_rects.append(load_button)

        boards_button = pg.Rect(self.screen_size[0] / 2 + 270, (self.screen_size[1] / 2 - self.logo.get_height() / 2) + 232, 130, 80)
        self.button_rects.append(boards_button)

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw(self.screen)
        return True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.menu_running = False
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        # Update the mouse position
        mouse_pos = pg.mouse.get_pos()
        mouse_actions = pg.mouse.get_pressed()  # 0 = left click
        self.mouse_rect = pg.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        # draw_text(self.screen, 'Game Title Here', 100, (255, 255, 255), (0, self.screen_size[1]*0.3))
        # draw_text(self.screen, 'ENTER to play', 60, (255, 255, 255), (0, self.screen_size[1]*0.5))

        # Draw the background
        for image in self.background_images:
            screen.blit(image, (0, 0))

        # Draw the logo
        X = self.screen_size[0] / 2 - self.logo.get_width() / 2
        Y = self.screen_size[1] / 2 - self.logo.get_height() / 2
        screen.blit(self.logo, (X, Y))

        # Draw the title text
        TITLE_OFFSET_X = 174
        TITLE_OFFSET_Y = 138
        draw_text(self.screen, 'The Woodcutter', 60, (255, 255, 255), (X+ TITLE_OFFSET_X, Y+TITLE_OFFSET_Y))

        # Draw the buttons
        # Debug rects
        for rect in self.button_rects:
            pg.draw.rect(self.screen, (0, 0, 255), rect)

        # Draw the button text
        draw_text(self.screen, 'Play', 60, (255, 255, 255), (X+368, Y + 232))
        draw_text(self.screen, 'Load', 36, (255, 255, 255), (X+68, Y + 250))
        draw_text(self.screen, 'Boards', 25, (255, 255, 255), (X+738, Y + 256))

        pg.display.flip()


class GameMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        self.playing = True

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw()
        return self.playing

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.menu_running = False
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.menu_running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        draw_text(self.screen, 'PAUSE', 100, (255, 255, 255), (0, self.screen_size[1]*0.3))
        draw_text(self.screen, 'ESC to quit, ENTER to play', 60, (255, 255, 255), (0, self.screen_size[1]*0.5))
        pg.display.flip()

