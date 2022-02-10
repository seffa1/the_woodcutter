import pygame as pg
from .utils import draw_text


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self, screen, player, dt, clock, level_manager):
        draw_text(screen, f'fps: {round(clock.get_fps())}', 25, (255, 0, 0), (3, 3))
        draw_text(screen, f'player pos: {player.pos}', 25, (255, 0, 0), (3, 23))
        draw_text(screen, f'p_rect pos: {player.rect.topleft}', 25, (255, 0, 0), (3, 43))
        draw_text(screen, f'vel pos: {player.vel}', 25, (255, 0, 0), (3, 63))
        draw_text(screen, f'action: {player.action}', 25, (255, 0, 0), (3, 83))
        draw_text(screen, f'Tile_Rects: {len(level_manager.tile_rects)}', 25, (255, 0, 0), (3, 103))
        draw_text(screen, f'DT: {round(dt, 2)}', 25, (255, 0, 0), (3, 123))
        draw_text(screen, f'Health: {player.health}', 25, (255, 0, 0), (3, 143))