import pygame as pg
import sys
from .utils import draw_text
import engine as e


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        player = e.Entity(screen.get_width()/2, screen.get_height()/2 - 30, 30, 35)

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
        self.screen.fill((0, 0, 0))

        draw_text(
            self.screen,
            f'fps: {round(self.clock.get_fps())}',
            25,
            (255, 255, 255),
            (10, 10)
        )

        pg.display.flip()