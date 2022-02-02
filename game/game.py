import pygame as pg
import sys
from .utils import draw_text
from .engine import Entity
from .entity_manager import Entity_Manager

# TODO
#   Frame Rate Independence

class Game:
    def __init__(self, screen, clock, display, WINDOW_SIZE):
        # Game setup
        self.screen = screen
        self.clock = clock
        self.display = display
        self.WINDOW_SIZE = WINDOW_SIZE
        self.width, self.height = self.screen.get_size()

        # Managers
        self.entity_manager = Entity_Manager()

        # Player
        self.player = Entity(100, 100, 30, 35, 'player')
        self.player.set_static_image('assets/animations/player/idle/idle_0.png')

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False

    def update(self):
        pass

    def draw(self):
        # Fill the background
        self.display.fill((0, 0, 0))

        # Draw player
        self.player.draw(self.display)

        # Draw the UI
        draw_text(
            self.display,
            f'fps: {round(self.clock.get_fps())}',
            25,
            (255, 255, 255),
            (10, 10)
        )

        self.screen.blit(pg.transform.scale(self.display, self.WINDOW_SIZE), (0, 0))

        pg.display.flip()