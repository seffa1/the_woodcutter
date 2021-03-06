import pygame as pg
from .utils import draw_text, Color
from .settings import SCALE_FACTOR_SETTING, DEV_TOOLS, FPS


class UI:
    def draw(self, screen, player, dt, clock, level_manager, scroll):
        # Dev tools
        if DEV_TOOLS:
            SIZE = 20
            X = 1300
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
            draw_text(screen, f'Charge damage: {player.damages["charge_up"]}', SIZE, (255, 0, 0), (X, 203))
            draw_text(screen, f'Damage: {player.damage}', SIZE, (255, 0, 0), (X, 223))
            # draw_text(screen, f'Collisions: {player.collision_types}', SIZE, (255, 0, 0), (900, 183))
            # draw_text(screen, f'Invincibility: {player.invincible}', SIZE, (255, 0, 0), (X, 163))

        if FPS:
            draw_text(screen, f'fps: {round(clock.get_fps())}', 20, (255, 0, 0), (1300, 3))

        # Health Bar
        health_rect = pg.Rect(15, 15, player.health * 2.5, 20)
        pg.draw.rect(screen, Color.HEALTH.value, health_rect)

        # Stamina Bar
        stamina_rect = pg.Rect(15, 35, player.stamina * 2.5, 20)
        pg.draw.rect(screen, Color.STAMINA.value, stamina_rect)

        # Coins
        draw_text(screen, f'Coins: {player.coins}', 25, (255, 0, 0), (15, 65))

        # Weapon Damage
        draw_text(screen, f"Damage: {player.damages['attack_1']}", 25, (255, 0, 0), (250, 65))

        # Charge attack bar
        charge_attack_rect = pg.Rect((player.pos.x - scroll[0]) * SCALE_FACTOR_SETTING,
                                     (player.pos.y - scroll[1] - 10) * SCALE_FACTOR_SETTING,
                                     player.damages['charge_up'], 10)
        pg.draw.rect(screen, Color.DAMAGE.value, charge_attack_rect)
