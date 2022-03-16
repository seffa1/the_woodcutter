from game.engine import Entity
import pygame as pg
from game.utils import calc_distance, Color, draw_text
from game.objects.coin import Coin
import random
from game.shop.shop_menu import Shop_Menu


class Old_Man(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0, rotate=None, entity_manager=None):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC, rotate)
        self.animation_frames['idle'] = self.load_animation('assets/animations/old_man/idle', [10, 10, 10, 10])
        self.animation_frames['walk'] = self.load_animation('assets/animations/old_man/walk', [10, 10, 10, 10, 10, 10])
        self.action = 'idle'

        # For buying items
        self.shop_menu = Shop_Menu(800, 380, 540, 330)
        self.show_menu = False
        self.can_talk = False  # Controlls when the 'but items' and 'talk' options are available, based on distance to the player

        # AI Controller use
        self.walk_left = False
        self.walk_right = False
        self.idle = True
        self.WALK_VEL = 1
        self.IDLE_RANGE = 70  # AI will go idle if player is within this range
        self.LOWER_X_BOUND = 660  # How far left hes allowed to go
        self.UPPER_X_BOUND = 900  # How far right he is allowed to go

    def AI_controller(self, player, dt):
        """ Uses a timer and randomness to walk back and forth. Has to stay within a certain distance from the store though. """
        # If idle, random chance to walk
        if self.idle:
            walk_chance = random.randint(0, 300)
            if walk_chance == 1:
                self.walk_left = True
                self.idle = False
            elif walk_chance == 2:
                self.walk_right = True
                self.idle = False

        # If walking, random chance to stop walking
        if self.walk_left or self.walk_right:
            idle_chance = random.randint(0, 300)
            if idle_chance <= 7:
                self.idle = True
                self.walk_left = False
                self.walk_right = False

        # If close to the player, go idle
        if calc_distance(self.pos.x, self.pos.y, player.pos.x, player.pos.y) < self.IDLE_RANGE:
            self.idle = True
            self.can_talk = True
            self.walk_right = False
            self.walk_left = False
        else:
            self.can_talk = False

        # If walking and hit an xbound, walk the other way
        if self.pos.x <= self.LOWER_X_BOUND:
            self.walk_right = True
            self.idle = False
        if self.pos.x >= self.UPPER_X_BOUND:
            self.walk_left = True
            self.idle = False

    def move(self, tile_rects, dt):
        self.vel.x = 0
        # Reset collisions
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}

        if self.walk_left:
            self.vel.x = -self.WALK_VEL
        if self.walk_right:
            self.vel.x = self.WALK_VEL

        self.pos.x += self.vel.x * dt
        self.rect.topleft = self.pos

        # Check for collisions in the x axis
        hit_list = self.collision_test(self.rect, tile_rects)
        for tile in hit_list:
            if self.vel.x > 0:
                self.collision_types['right'] = True
                self.rect.right = tile.left
                self.pos.x = self.rect.topleft[0]
            if self.vel.x < 0:
                self.collision_types['left'] = True
                self.rect.left = tile.right
                self.pos.x = self.rect.topleft[0]

        # Y axis
        self.acc.y = self.GRAV * dt
        self.vel.y += self.acc.y
        if self.vel.y > self.MAX_FALL_SPEED:
            self.vel.y = self.MAX_FALL_SPEED
        self.pos.y += self.vel.y * dt
        self.rect.topleft = self.pos

        # Check for collisions in the y axis
        hit_list = self.collision_test(self.rect, tile_rects)
        for tile in hit_list:
            # If you are falling
            if self.vel.y > 0:
                self.collision_types['bottom'] = True
                self.rect.bottom = tile.top  # Change the rect's position because of convientient methods
                self.pos.y = self.rect.topleft[1]
                self.vel.y = 1
            if self.vel.y < 1:
                self.collision_types['top'] = True
                self.rect.top = tile.bottom
                self.pos.y = self.rect.topleft[1]
                self.vel.y = 0

        # Updates from y-axis collisions
        if self.collision_types['bottom'] or self.collision_types['right'] or self.collision_types['left']:
            self.air_timer_float = 0
            self.wall_jump_timer = 0
            self.jumping = False
        else:
            self.air_timer_float += 1 * dt
            self.air_timer = int(round(self.air_timer_float, 0))

    def actions(self, dt):
        """ Determine the current action and update the image accordingly """
        walk_threshold = .2
        # Flip check
        if self.vel.x > 0:
            self.flip = False
        if self.vel.x < 0:
            self.flip = True

        # Idle check
        if abs(self.vel.x) <= walk_threshold:
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'idle')

        # Walking / Running Check
        if self.vel.x > walk_threshold:
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'walk')
        if self.vel.x < -walk_threshold:
            self.action, self.frame, self.frame_float = self.change_actions(self.action, self.frame, self.frame_float, 'walk')

    def set_image(self, dt):
        """ Update the current image """
        self.frame_float += 1 * dt
        self.frame = int(round(self.frame_float, 0))

        # If your animation frames come to an end
        if self.frame >= len(self.animation_frames[self.action]):
            self.frame = 0
            self.frame_float = 0

        image_id = self.animation_frames[self.action][self.frame]
        image = self.animation_images[image_id]
        self.image = image

    def update(self, tile_rects, dt, player=None):
        if self.show_menu:
            self.shop_menu.update(tile_rects, dt, player)

        self.AI_controller(player, dt)  # Updates the actions based on player's location
        self.move(tile_rects, dt)  # Update entity position
        self.actions(dt)  # Determine the entities's action
        self.set_image(dt)  # Set the image based on the action

    def draw(self, display, scroll, hitbox=False, attack_box=False):
        if hitbox:
            hit_rect = pg.Rect(self.pos.x - scroll[0], self.pos.y - scroll[1], self.rect.width, self.rect.height)
            pg.draw.rect(display, (0, 255, 0), hit_rect)

        # Flip the image if we need to, and then blit it
        image = pg.transform.flip(self.image, self.flip, False)
        display.blit(image, (self.pos.x - scroll[0], self.pos.y - scroll[1]))

    def draw_menu(self, display, scroll, screen):
        """ This gets called independently from the draw function as it is drawing to the screen, not the display. """
        if self.can_talk:
            draw_text(screen, f'1: Talk', 50, (255, 255, 255), (15, 815))
            draw_text(screen, f'2: Shop', 50, (255, 255, 255), (500, 815))

            # Draw the menu
            if self.show_menu:

                self.shop_menu.draw(display, scroll, screen, hitbox=False, attack_box=False)
        else:
            self.show_menu = False

    def toggle_menu(self):
        """ Called from the game's event loop. """
        if self.show_menu:
            self.show_menu = False
        else:
            self.show_menu = True

