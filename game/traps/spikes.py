import pygame as pg
from game.engine import Entity


class Spikes(Entity):
    """ Spikes that can be placed on the ground, walls, or ceiling which can retract """
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC)

        # How many frames must go by for the spikes to retract, and then expand again
        self.spike_rate = 0
        self.DAMAGE = 0
        self.retract = False
        self.action = None


    def check_damages(self, player):
        # Check if we have taken damage
        if player.attack_rect:
            if self.rect.colliderect(player.attack_rect):
                self.lose_health(player.damage)

        # Check if we have damaged the player
        if self.attack_rect:
            if self.attack_rect.colliderect(player.rect):
                player.lose_health(self.damage)

    def hitboxes(self, dt):
        if not self.attacking:
            self.damage = 0
            return

        if self.attack['1']:
            self.damage = self.DAMAGES['attack_1']
            self.attack_1_timer_float += 1 * dt
            self.attack_1_timer = int(round(self.attack_1_timer_float, 0))
            # self.attack_1_timer += 1

            if self.attack_1_timer > 15:  # 10 is to be adjusted as we go
                if not self.flip:
                    self.attack_rect = pg.Rect(self.rect.right - 25, self.rect.centery - 8, 45, 30)
                else:
                    self.attack_rect = pg.Rect(self.rect.left - 15, self.rect.centery - 8, 45, 30)
            if self.attack_1_timer > 20:
                self.attack_rect = None

    def update(self, tile_rects, dt, player=None):
        self.move(tile_rects, dt)  # Update entity position
        # self.actions(dt)  # Determine the entities's action
        # self.set_image(dt)  # Set the image based on the action
        self.hitboxes(dt)  # Update any hit boxes from attack
        self.check_damages(player)

    def draw(self, display, scroll, hitbox=True, attack_box=False):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)


        # Flip the image if we need to, and then blit it
        # player_image = pg.transform.flip(self.image, self.flip, False)
        # display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        if attack_box:
            if self.attack_rect is not None:
                attack_rect_scrolled = pg.Rect(self.attack_rect.x - scroll[0],
                                                        self.attack_rect.y - scroll[1],
                                                        self.attack_rect.width, self.attack_rect.height)
                pg.draw.rect(display, (255, 0, 0), attack_rect_scrolled)