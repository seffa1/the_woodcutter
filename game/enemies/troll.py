from game.engine import Entity
import pygame as pg
from game.utils import calc_distance, Color
from game.objects.coin import Coin




class Troll(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['idle'] = self.load_animation('assets/animations/troll/idle', [10, 10, 10, 10], True)
        self.animation_frames['walk'] = self.load_animation('assets/animations/troll/walk', [10, 10, 10, 10, 10, 10], True)
        self.animation_frames['attack_1'] = self.load_animation('assets/animations/troll/attack_1', [3, 4, 7, 7, 4, 4], True)
        self.animation_frames['death'] = self.load_animation('assets/animations/troll/death', [10, 10, 20, 60, 120], True)
        self.animation_frames['hurt'] = self.load_animation('assets/animations/troll/hurt', [5, 20], True)

        # Troll Stats
        self.health = 100
        self.MAX_HEALTH = 100

        # AI Constants
        self.DAMAGES = {'attack_1': 25}
        self.DAMAGE_COOLDOWN = 25  # How many frames you are invinciple for after taking damage
        self.AGGRO_RANGE = 200
        self.DEAGGRO_RANGE = 400
        self.ATTACK_RANGE = 30
        self.ATTACK_COOLDOWN = 90

        # AI Controller use
        self.aggro = False
        self.attack_timer = 0  # Used when we are not in aggro
        self.attack_timer_float = 0

    def AI_controller(self, player, dt):
        if self.death:
            return

        if not self.aggro:
            self.walk_right = False
            self.walk_left = False
            self.attack_timer = 0
            self.attack_timer_float = 0

        else:
            if player.rect.center[0] < (self.rect.center[0] - self.ATTACK_RANGE) and not self.attacking:
                self.walk_right = False
                self.walk_left = True
                self.attack_timer_float -= 1 * dt
                self.attack_timer = int(round(self.attack_timer_float, 0))
                if self.attack_timer_float < 0:
                    self.attack_timer_float = 0
                if self.attack_timer < 0:
                    self.attack_timer = 0

            if player.rect.center[0] > (self.rect.center[0] + self.rect.width + self.ATTACK_RANGE) and not self.attacking:
                self.walk_left= False
                self.walk_right = True
                self.attack_timer_float -= 1 * dt
                self.attack_timer = int(round(self.attack_timer_float, 0))
                if self.attack_timer_float < 0:
                    self.attack_timer_float = 0
                if self.attack_timer < 0:
                    self.attack_timer = 0

            # Attack Left
            if (self.rect.center[0] - self.ATTACK_RANGE) < player.rect.center[0] <= self.rect.center[0]:
                self.walk_right = False
                self.walk_left = False
                self.flip = True
                if self.attack_timer <= 1 and not self.hurt:
                    self.attacking = True
                    self.attack['1'] = True
                    self.attack_timer = self.ATTACK_COOLDOWN
                    self.attack_timer_float = self.ATTACK_COOLDOWN
                else:
                    self.attack_timer_float -= 1 * dt
                    self.attack_timer = int(round(self.attack_timer_float, 0))
                    if self.attack_timer_float < 0:
                        self.attack_timer_float = 0
                    if self.attack_timer < 0:
                        self.attack_timer = 0

            # Attack Right
            if self.rect.center[0] < player.rect.center[0] < (self.rect.center[0] + self.ATTACK_RANGE):
                self.walk_right = False
                self.walk_left = False
                self.flip = False
                if self.attack_timer <= 1 and not self.hurt:
                    self.attacking = True
                    self.attack['1'] = True
                    self.attack_timer = self.ATTACK_COOLDOWN
                    self.attack_timer_float = self.ATTACK_COOLDOWN
                else:
                    self.attack_timer_float -= 1 * dt
                    self.attack_timer = int(round(self.attack_timer_float, 0))
                    if self.attack_timer_float < 0:
                        self.attack_timer_float = 0
                    if self.attack_timer < 0:
                        self.attack_timer = 0

    def check_aggro(self, player):
        """ Checks if the player is within certain aggro distances """
        if calc_distance(self.rect.center[0], self.rect.center[1], player.rect.center[0], player.rect.center[1]) <= self.AGGRO_RANGE:
            self.aggro = True
        if calc_distance(self.rect.center[0], self.rect.center[1], player.rect.center[0], player.rect.center[1]) >= self.DEAGGRO_RANGE:
            self.aggro = False

    def drop_loot(self):
        """ This function must be defined the the children classes """
        # Instantiate a coin which has velocity and collision to the ground?
        pass

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

    def check_damages(self, player):
        # Check if we have taken damage
        if player.attack_rect:
            if self.rect.colliderect(player.attack_rect):
                self.lose_health(player.damage)

        # Check if we have damaged the player
        if self.attack_rect:
            if self.attack_rect.colliderect(player.rect):
                player.lose_health(self.damage)

    def update(self, tile_rects, dt, player=None):
        self.check_aggro(player)  # update the aggro state of the entity
        self.AI_controller(player, dt)  # Updates the actions based on player's location
        self.move(tile_rects, dt)  # Update entity position
        self.actions(dt)  # Determine the entities's action
        self.set_image(dt)  # Set the image based on the action
        self.hitboxes(dt)  # Update any hit boxes from attack
        self.check_damages(player)

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)


        # Flip the image if we need to, and then blit it
        player_image = pg.transform.flip(self.image, self.flip, False)
        display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        # Draw the health bar
        health_bar = pg.Rect(self.rect.center[0] - scroll[0] - (self.MAX_HEALTH/4), self.pos.y - scroll[1] - 10, self.health / 2, 5)
        pg.draw.rect(display, Color.HEALTH.value, health_bar)


        if attack_box:
            if self.attack_rect is not None:
                attack_rect_scrolled = pg.Rect(self.attack_rect.x - scroll[0],
                                                        self.attack_rect.y - scroll[1],
                                                        self.attack_rect.width, self.attack_rect.height)
                pg.draw.rect(display, (255, 0, 0), attack_rect_scrolled)