import pygame as pg
import math


def draw_text(screen, text, size, colour, pos):

    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)


def calc_distance(x1, y1, x2, y2):
    """ Returns the distance between two positional vectors (pg.math.Vector2) """
    return int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
