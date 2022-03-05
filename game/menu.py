import pygame as pg
import sys
from .utils import *
from .Save_Load_Manager import Save_Load_Manager
# from .settings import WINDOW_SIZE



class StartMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()

        self.logo = pg.transform.scale(pg.image.load('assets/images/ui/Logo.png').convert_alpha(), (900, 390))

        self.background_images = []  # List of background images (since they are setup for paralax)
        self.load_background('forest_4', 7)

        # Rects
        self.mouse_rect = None
        self.button_rects = []
        self.load_buttons()

        # Colors
        self.DEFAULT_COLOR = (255, 255, 255)
        self.HOVER_COLOR = (0, 200, 15)
        self.play_color = self.DEFAULT_COLOR
        self.load_color = self.DEFAULT_COLOR
        self.boards_color = self.DEFAULT_COLOR

        # Saving and Loading Manager
        self.save_load_manager = Save_Load_Manager('.wood', 'save_data')

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
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        # Update the mouse position
        mouse_pos = pg.mouse.get_pos()
        mouse_actions = pg.mouse.get_pressed()  # 0 = left click
        self.mouse_rect = pg.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

        # If you left click
        if mouse_actions[0]:
            # Play button
            if self.mouse_rect.colliderect(self.button_rects[0]):
                self.menu_running = False
            # Load button
            elif self.mouse_rect.colliderect(self.button_rects[1]):
                print("Loading game...")

                # Extract game data
                load_data = self.save_load_manager.load('Saved_Game')

                # Pass game data to the main file

                # Main file passes the load data into the game

                # Game checks if it has load data on start up

                # Builds the game with the data

            # Boards button
            elif self.mouse_rect.colliderect(self.button_rects[2]):
                print("Loading Leaderboards...")

        # Update text colors if you hover over them
        if self.mouse_rect.colliderect(self.button_rects[0]):
            self.play_color = self.HOVER_COLOR
        else:
            self.play_color = self.DEFAULT_COLOR
        if self.mouse_rect.colliderect(self.button_rects[1]):
            self.load_color = self.HOVER_COLOR
        else:
            self.load_color = self.DEFAULT_COLOR
        if self.mouse_rect.colliderect(self.button_rects[2]):
            self.boards_color = self.HOVER_COLOR
        else:
            self.boards_color = self.DEFAULT_COLOR

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

        # Draw the button text
        draw_text(self.screen, 'Play', 60, self.play_color, (X+368, Y + 232))
        draw_text(self.screen, 'Load', 36, self.load_color, (X+68, Y + 250))
        draw_text(self.screen, 'Boards', 25, self.boards_color, (X+738, Y + 256))

        pg.display.flip()


class GameMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        self.playing = True

        self.logo = pg.transform.scale(pg.image.load('assets/images/ui/Logo.png').convert_alpha(), (900, 390))
        self.control_frame = pg.transform.scale(pg.image.load('assets/images/ui/controls_frame.png'), (576, 650))

        self.background_images = []  # List of background images (since they are setup for paralax)
        self.load_background('forest_4', 7)

        # Rects
        self.mouse_rect = None
        self.button_rects = []
        self.load_buttons()

        # Colors
        self.DEFAULT_COLOR = (255, 255, 255)
        self.HOVER_COLOR = (0, 200, 15)
        self.play_color = self.DEFAULT_COLOR
        self.load_color = self.DEFAULT_COLOR
        self.boards_color = self.DEFAULT_COLOR

        # Saving and Loading Manager
        self.save_load_manager = Save_Load_Manager('.wood', 'save_data')

    def load_buttons(self):
        play_button = pg.Rect(self.screen_size[0] / 2 - 138, (self.screen_size[1] / 2 - self.logo.get_height() / 2) + 232, 260, 100)
        self.button_rects.append(play_button)

        load_button = pg.Rect(self.screen_size[0] / 2 - 400, (self.screen_size[1] / 2 - self.logo.get_height() / 2) + 232, 130, 100)
        self.button_rects.append(load_button)

        boards_button = pg.Rect(self.screen_size[0] / 2 + 270, (self.screen_size[1] / 2 - self.logo.get_height() / 2) + 232, 130, 80)
        self.button_rects.append(boards_button)

    def load_background(self, name: str, qty: int):
        path = 'assets/images/backgrounds/' + name + '/'
        for i in range (1, qty + 1):
            image = pg.image.load(path + str(i) + '.png')
            self.background_images.append(image)

    def run(self, game):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.events()
            self.update(game)
            self.draw(self.screen)
        return self.playing

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.menu_running = False

    def update(self, game):
        # Update the mouse position
        mouse_pos = pg.mouse.get_pos()
        mouse_actions = pg.mouse.get_pressed()  # 0 = left click
        self.mouse_rect = pg.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

        # If you left click
        if mouse_actions[0]:
            # Play button
            if self.mouse_rect.colliderect(self.button_rects[0]):
                self.menu_running = False
            # Quit button
            elif self.mouse_rect.colliderect(self.button_rects[1]):
                self.playing = False
                self.menu_running = False

            # Save button
            elif self.mouse_rect.colliderect(self.button_rects[2]):
                print("Saving Game...")

                # Need to extract the meta data from the game
                self.save_load_manager.save(game, 'Saved_Game')


        # Update text colors if you hover over them
        if self.mouse_rect.colliderect(self.button_rects[0]):
            self.play_color = self.HOVER_COLOR
        else:
            self.play_color = self.DEFAULT_COLOR
        if self.mouse_rect.colliderect(self.button_rects[1]):
            self.load_color = self.HOVER_COLOR
        else:
            self.load_color = self.DEFAULT_COLOR
        if self.mouse_rect.colliderect(self.button_rects[2]):
            self.boards_color = self.HOVER_COLOR
        else:
            self.boards_color = self.DEFAULT_COLOR

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
        TITLE_OFFSET_X = 230
        TITLE_OFFSET_Y = 138
        draw_text(self.screen, 'Game Paused', 60, (255, 255, 255), (X + TITLE_OFFSET_X, Y + TITLE_OFFSET_Y))

        # Draw the button text
        draw_text(self.screen, 'Play', 60, self.play_color, (X + 368, Y + 232))
        draw_text(self.screen, 'Quit', 36, self.load_color, (X + 68, Y + 250))
        draw_text(self.screen, 'Save', 25, self.boards_color, (X + 753, Y + 256))

        # Draw the controls frame
        screen.blit(self.control_frame, (self.screen_size[0] / 2 - self.control_frame.get_width() / 2,650))
        CONTROLS_OFFSET = 40
        draw_text(self.screen, 'Move Left -----> A', 36, (255, 255, 255), (X + 200, Y + 400))
        draw_text(self.screen, 'Move Right ----> D', 36, (255, 255, 255), (X + 200, Y + 400 + CONTROLS_OFFSET))
        draw_text(self.screen, 'Jump ----------> W', 36, (255, 255, 255), (X + 200, Y + 400 + CONTROLS_OFFSET * 2))
        draw_text(self.screen, 'Roll ----------> Space', 36, (255, 255, 255), (X + 200, Y + 400 + CONTROLS_OFFSET * 3))
        draw_text(self.screen, 'Attack (Hold) -> C', 36, (255, 255, 255), (X + 200, Y + 400 + CONTROLS_OFFSET * 4))

        pg.display.flip()

