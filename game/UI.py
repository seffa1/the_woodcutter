import pygame as pg
from .utils import draw_text, Color
from enum import Enum


class UI:
    def __init__(self):
        self.dev_tools = True

    def draw(self, screen, player, dt, clock, level_manager):
        # Dev tools
        if self.dev_tools:
            SIZE = 20
            X = 1300
            draw_text(screen, f'fps: {round(clock.get_fps())}', SIZE, (255, 0, 0), (X, 3))
            draw_text(screen, f'player pos: {player.pos}', SIZE, (255, 0, 0), (X, 23))
            draw_text(screen, f'p_rect pos: {player.rect.topleft}', SIZE, (255, 0, 0), (X, 43))
            draw_text(screen, f'vel pos: {player.vel}', SIZE, (255, 0, 0), (X, 63))
            draw_text(screen, f'action: {player.action}', SIZE, (255, 0, 0), (X, 83))
            draw_text(screen, f'Tile_Rects: {len(level_manager.tile_rects)}', SIZE, (255, 0, 0), (X, 103))
            draw_text(screen, f'DT: {round(dt, 2)}', SIZE, (255, 0, 0), (X, 123))
            draw_text(screen, f'Health: {player.health}', SIZE, (255, 0, 0), (X, 143))
            draw_text(screen, f'Air Timer: {player.air_timer}', SIZE, (255, 0, 0), (X, 163))
            mouse_pos = pg.mouse.get_pos()
            draw_text(screen, f'Mouse Pos: {mouse_pos}', SIZE, (255, 0, 0), (X, 183))
            # draw_text(screen, f'Collisions: {player.collision_types}', SIZE, (255, 0, 0), (900, 183))
            # draw_text(screen, f'Invincibility: {player.invincible}', SIZE, (255, 0, 0), (X, 163))

        # Health Bar
        health_rect = pg.Rect(15, 15, player.health * 2.5, 20)
        pg.draw.rect(screen, Color.HEALTH.value, health_rect)

        # Stamina Bar
        stamina_rect = pg.Rect(15, 35, player.stamina * 2.5, 20)
        pg.draw.rect(screen, Color.STAMINA.value, stamina_rect)

        # Coins
        draw_text(screen, f'Coins: {player.coins}', 25, (255, 0, 0), (15, 65))

        # Weapon Damage
        draw_text(screen, f"Damage: {player.DAMAGES['attack_1']}", 25, (255, 0, 0), (250, 65))
