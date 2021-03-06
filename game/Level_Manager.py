import random
import pygame as pg
from .utils import draw_text, Color
from .Level import Level
from .Time_Manager import Time_Manager
from .audio_manager import Audio_Manager
from .settings import SCALE_FACTOR_SETTING


class Level_Manager:
    def __init__(self):
        self.levels = {}
        self.current_level = '0-1'

        # Prevents play from triggering triggers many times due to the hitbox colliding
        self.level_change_timer = 0
        self.CHANGE_COOLDOWN = 60

        # Calls down to the current level's tile manager, and gets updated collidable rects each framee
        self.tile_rects = []
        self.collided_trigger = None

        # Create time manager to keep track of each levels best timers
        self.time_manager = Time_Manager()

        # Audio Manager
        self.audio_manager = Audio_Manager()
        self.audio_manager.play_music(random.choice(['Home_Music_1', 'Home_Music_2']))

    def load_level(self, ID: str, TILE_SIZE: int, display):
        self.levels[ID] = Level(ID, TILE_SIZE, display)

    def set_level(self, ID: str, player):
        """ Changes the current level getting updated, then moves the player to that levels respawn point.
         Queues the music as well. """
        # Change level
        if ID not in self.levels:
            raise "You are trying to set to a level that does not exist"

        # Queue the music, only if its a differnet level (so it doesnt restart on a respawn)
        if ID[0] != self.current_level[0]:
            if ID == '0-1':
                self.audio_manager.play_music(random.choice(['Home_Music_1', 'Home_Music_2']))
            else:
                self.audio_manager.play_music(random.choice(['Battle_Music_1', 'Battle_Music_2', 'Battle_Music_3']))

        # Set the new level
        self.current_level = ID
        level = self.get_level()
        # Generate the enemies for that level
        level.entity_manager.load_enemies()
        # Move player to spawn point
        player.set_position(level.respawn_point[0], level.respawn_point[1])

    def check_change_level(self, player):
        """ Only gets called when the player presses enter from the game event loop,
        then checks if a player is colliding with a level trigger. """
        # Check if player hit the trigger
        if not self.get_level().collided_trigger:
            return

        if self.level_change_timer > 0:
            return

        # Check if all enemies on the level are dead and all collectibles collected
        for group in self.get_level().entity_manager.groups.values():
            for entity in group:
                if entity.type in ['troll', 'collectible']:
                    return

        trigger = self.get_level().collided_trigger
        self.set_level(trigger.level_to_go_to, player)

        # If its the starting level in a world, start the timer
        if trigger.level_to_go_to in ['1-1', '2-1', '3-1']:
            self.time_manager.start_timer(trigger.level_to_go_to)

        # If we are going back to the main world, stop the timer
        if trigger.level_to_go_to == '0-1':
            self.time_manager.stop_timer()

        # Add cooldown for level changing
        self.level_change_timer = self.CHANGE_COOLDOWN

    def get_level(self):
        """ Returns the current level object """
        return self.levels[self.current_level]

    def update(self, player, dt):
        self.level_change_timer -= 1
        self.tile_rects = self.get_level().tile_manager.tile_rects
        self.get_level().update(player, self.tile_rects, dt)
        self.check_change_level(player)

    # Drawing ----------------------------------------------------------------------------------------------------------
    def draw_enemy_collectibles_left(self, screen):
        """ Tells player how many enemies and collectibles are left on the level"""
        if self.current_level == '0-1':
            return

        level = self.get_level()
        enemies = level.entity_manager.groups.get('troll')
        if enemies:
            draw_text(screen, f'Enemies Remaining: {len(enemies)}', 25, Color.DAMAGE.value, (700, 50))

        collectibles = level.entity_manager.groups.get('collectible')
        if collectibles:
            draw_text(screen, f'Orbs Remaining: {len(collectibles)}', 25, Color.DAMAGE.value, (700, 80))

    def draw_background(self, scroll, display):
        self.get_level().draw_background(scroll, display)

    def draw_tiles(self, scroll, TILE_SIZE, display):
        self.get_level().draw_tiles(scroll, TILE_SIZE, display)

    def draw_entities(self, scroll, display, screen):
        self.get_level().draw_entities(scroll, display, screen)

    def draw_triggers(self, scroll, display):
        self.get_level().draw_triggers(scroll, display)

    def draw_cave_entrances(self, scroll, screen):
        if self.current_level == '0-1':
            image = pg.transform.scale(pg.image.load('assets/images/misc/cave_entrance.png').convert_alpha(), (484, 220))
            screen.blit(image, ((-scroll[0] + 312) * SCALE_FACTOR_SETTING, (-scroll[1] + 192) * SCALE_FACTOR_SETTING))
            screen.blit(image, ((-scroll[0] + 910) * SCALE_FACTOR_SETTING, (-scroll[1] + 312) * SCALE_FACTOR_SETTING))
            # screen.blit(image, (600, 200))

    def draw_timer(self, screen):
        self.time_manager.draw_timer(screen)



