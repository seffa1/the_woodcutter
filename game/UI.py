import pygame as pg
from .utils import draw_text, Color
from enum import Enum


class UI:
    def __init__(self):
        self.dev_tools = True

    def draw(self, screen, player, dt, clock, level_manager):
        # Dev tools
        if self.dev_tools:
            draw_text(screen, f'fps: {round(clock.get_fps())}', 25, (255, 0, 0), (1400, 3))
            draw_text(screen, f'player pos: {player.pos}', 25, (255, 0, 0), (1400, 23))
            draw_text(screen, f'p_rect pos: {player.rect.topleft}', 25, (255, 0, 0), (1400, 43))
            draw_text(screen, f'vel pos: {player.vel}', 25, (255, 0, 0), (1400, 63))
            draw_text(screen, f'action: {player.action}', 25, (255, 0, 0), (1400, 83))
            draw_text(screen, f'Tile_Rects: {len(level_manager.tile_rects)}', 25, (255, 0, 0), (1400, 103))
            draw_text(screen, f'DT: {round(dt, 2)}', 25, (255, 0, 0), (1400, 123))
            draw_text(screen, f'Health: {player.health}', 25, (255, 0, 0), (1400, 143))
            draw_text(screen, f'Air Timer: {player.air_timer}', 25, (255, 0, 0), (1400, 163))
            # draw_text(screen, f'Collisions: {player.collision_types}', 25, (255, 0, 0), (900, 183))

            # draw_text(screen, f'Invincibility: {player.invincible}', 25, (255, 0, 0), (1400, 163))

        # Health Bar
        health_rect = pg.Rect(15, 15, player.health * 2.5, 20)
        pg.draw.rect(screen, Color.HEALTH.value, health_rect)

        # Stamina Bar
        stamina_rect = pg.Rect(15, 35, player.stamina * 2.5, 20)
        pg.draw.rect(screen, Color.STAMINA.value, stamina_rect)

        # Coins
        draw_text(screen, f'Coins: {player.coins}', 35, (255, 0, 0), (15, 65))
