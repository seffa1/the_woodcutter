from game.engine import Entity
import pygame as pg
from game.utils import calc_distance



class Troll(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC)
        self.animation_frames['idle'] = self.load_animation('assets/animations/troll/idle', [10, 10, 10, 10], True)
        self.animation_frames['walk'] = self.load_animation('assets/animations/troll/walk', [10, 10, 10, 10, 10, 10], True)
        self.animation_frames['attack_1'] = self.load_animation('assets/animations/troll/attack_1', [10, 10, 10, 10, 10, 10], True)
        self.animation_frames['death'] = self.load_animation('assets/animations/troll/death', [10, 10, 10, 10, 10], True)

        # AI Constants
        self.AGGRO_RANGE = 200
        self.DEAGGRO_RANGE = 400
        self.ATTACK_RANGE = 40


        # AI Controller use
        self.aggro = False
        self.idle_timer = 0  # Used when we are not in aggro

    def AI_controller(self, player):
        if not self.aggro:
            self.walk_right = False
            self.walk_left = False

        else:
            if player.pos.x < (self.pos.x - self.ATTACK_RANGE):
                self.walk_left = True

            if player.pos.x > (self.pos.x + self.rect.width + self.ATTACK_RANGE):
                self.walk_right = True

            if (self.pos.x - self.ATTACK_RANGE) < player.pos.x <= self.pos.x:
                self.walk_right = False
                self.walk_left = False
                self.attacking = True
                self.attack['1'] = True
                self.flip = True

            if self.pos.x < player.pos.x < (self.pos.x + self.rect.width + self.ATTACK_RANGE):
                self.walk_right = False
                self.walk_left = False
                self.attacking = True
                self.attack['1'] = True
                self.flip = False

    def check_aggro(self, player):
        """ Checks if the player is within certain aggro distances """
        if calc_distance(self.pos, player.pos) <= self.AGGRO_RANGE:
            self.aggro = True
            print("Troll aggro")
        if calc_distance(self.pos, player.pos) >= self.DEAGGRO_RANGE:
            self.aggro = False
            print("Troll de-aggro")

    def hitboxes(self, dt):
        if not self.attacking:
            return

        if self.attack['1']:
            self.attack_1_timer_float += 1 * dt
            self.attack_1_timer = int(round(self.attack_1_timer_float, 0))
            # self.attack_1_timer += 1

            if self.attack_1_timer > 24:  # 10 is to be adjusted as we go
                if not self.flip:
                    self.attack_rect = pg.Rect(self.rect.right, self.rect.centery - 8, 10, 23)
                else:
                    self.attack_rect = pg.Rect(self.rect.left, self.rect.centery - 8, 10, 23)
            if self.attack_1_timer > 30:
                self.attack_rect = None


    def update(self, tile_rects, dt, player=None):
        self.check_aggro(player)  # update the aggro state of the entity
        self.AI_controller(player)  # Updates the actions based on player's location
        self.move(tile_rects, dt)  # Update entity position
        self.actions()  # Determine the entities's action
        self.set_image(dt)  # Set the image based on the action
        self.hitboxes(dt)  # Update any hit boxes from attack

    def draw(self, display, scroll, hitbox=True, attack_box=True):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)


        # Flip the image if we need to, and then blit it
        player_image = pg.transform.flip(self.image, self.flip, False)
        display.blit(player_image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

        if attack_box:
            if self.attack_rect is not None:
                attack_rect_scrolled = pg.Rect(self.attack_rect.x - scroll[0],
                                                        self.attack_rect.y - scroll[1],
                                                        self.attack_rect.width, self.attack_rect.height)
                pg.draw.rect(display, (255, 0, 0), attack_rect_scrolled)