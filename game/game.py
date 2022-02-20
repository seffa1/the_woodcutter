import pygame as pg
import sys, time
from .Level_Manager import Level_Manager
from .player import Player
from .UI import UI


# TODO
#   Level up menu to spend coins
#   Add double jump capabilities
#   Finish a level loop (figure out how items respawn or dont respawn ecah run, timers, medals?)
#   Fix animation images to they are centered on the character
#   Fix menu sizes, polish them, adding controls to both menus
#   Batch Rendering of ground for less collisions checks
#   Only checking collisions on tiles close to player (Add chunk rendering?)

vec = pg.math.Vector2


class Game:
    def __init__(self, screen, clock, display, WINDOW_SIZE, SCALE_FACTOR):
        # Game setup
        self.screen = screen
        self.clock = clock
        self.display = display
        self.FPS = 60
        self.WINDOW_SIZE = WINDOW_SIZE
        self.SCALE_FACTOR = SCALE_FACTOR
        self.TILE_SIZE = 24
        self.width, self.height = self.screen.get_size()
        self.dt = 0

        # Camera Scroll
        self.true_scroll = [0, 0]  # The scroll as a percise float
        self.scroll = [0, 0]  # The scroll rounded to an int
        self.OFFSET_X = WINDOW_SIZE[0] / SCALE_FACTOR / 2
        self.OFFSET_Y = WINDOW_SIZE[1] / SCALE_FACTOR / 3 * 2

        # Player
        self.player = Player(703, 229, 30, 35, 'player', WALK_ACC=.3, FRIC=-.15)

        # Managers
        self.level_manager = Level_Manager()
        self.level_manager.load_level('0-1', self.TILE_SIZE, display)
        self.level_manager.load_level('0-2', self.TILE_SIZE, display)
        self.level_manager.load_level('3-1', self.TILE_SIZE, display)
        self.level_manager.set_level('0-1', self.player)

        # Player
        self.player = Player(703, 229, 30, 35, 'player', WALK_ACC=.3, FRIC=-.15)

        # User Interface
        self.UI = UI()

    def run(self):
        self.playing = True
        self.last_time = time.time()  # For frame rate independence
        while self.playing:

            # Frame rate independence check. Finds how many seconds have passed since the last frame.
            # If we are at 60 fps, dt will be 0-1/60th of a second
            # Multiply it by 60 so if we are at 60 fps, dt is 1, If we ran at 30 fps, dt would be 2/60th * 60 = 2.
            # So everything that moves get multiplied by 2, animation frames get cycled at a factor of 2
            self.dt = time.time() - self.last_time
            self.dt *= 60
            self.last_time = time.time()

            self.events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Check respawn
            if event.type == pg.USEREVENT + 1:
                self.player.health = self.player.max_health
                self.player.action = 'idle'
                self.player.death = False
                # self.level_manager.get_level().respawn_level()

                self.level_manager.set_level(self.level_manager.current_level, self.player)
                self.player.set_position(self.level_manager.get_level().respawn_point[0],
                                         self.level_manager.get_level().respawn_point[1])
                self.player.health = self.player.max_health
                self.player.stamina = self.player.max_stamina
                self.player.stamina_float = self.player.max_stamina


            # Check special keys
            mods = pg.key.get_mods()
            if mods & pg.KMOD_SHIFT and self.player.stamina > self.player.STAMINA_RUN_DRAIN:
                self.player.run = True
            else:
                self.player.run = False

            # Check the rest of the keys
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                if event.key == pg.K_d:
                    self.player.walk_right = True
                if event.key == pg.K_a:
                    self.player.walk_left = True
                if event.key == pg.K_w and not self.player.roll:  # Cant jump while rolling
                    if self.player.stamina >= self.player.STAMINA_USE['jump']:
                        if not self.player.jumping:
                            self.player.use_stamina(self.player.STAMINA_USE['jump'])
                        self.player.jump()

                # Cant roll unless on the ground
                if event.key == pg.K_SPACE and not self.player.roll and self.player.collision_types['bottom'] and not self.player.attacking:
                    if self.player.stamina >= self.player.STAMINA_USE['roll']:
                        self.player.roll = True
                        self.player.invincible = True
                        self.player.invincible_timer = self.player.INVINCIBLE_FRAMES
                        self.player.invincible_timer_float = self.player.INVINCIBLE_FRAMES
                        self.player.use_stamina(self.player.STAMINA_USE['roll'])
                # Cant attack while rolling
                if event.key == pg.K_c and not self.player.roll:
                    if self.player.stamina >= self.player.STAMINA_USE['attack_1']:
                        self.player.attacking = True
                        self.player.attack['1'] = True
                        self.player.use_stamina(self.player.STAMINA_USE['attack_1'])
                if event.key == pg.K_RETURN:
                    self.level_manager.check_change_level(self.player)

            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    self.player.walk_right = False
                if event.key == pg.K_a:
                    self.player.walk_left = False
                if event.key == pg.K_w:
                    if self.player.vel.y < -1:
                        self.player.vel.y = -1

    def update(self):
        # Scroll
        # Sets the "cameras" position. The divisor adds the lagging behind, smoothing effect
        self.true_scroll[0] += (self.player.rect.x - self.true_scroll[0] - self.OFFSET_X) / 10
        self.true_scroll[1] += (self.player.rect.y - self.true_scroll[1] - self.OFFSET_Y) / 10
        scroll = self.true_scroll.copy()
        # Rounds the float to an int for the drawings not to get choppy
        self.scroll[0] = int(scroll[0])
        self.scroll[1] = int(scroll[1])

        # Update the level manager: Updates world tiles, and all entities except the player
        self.level_manager.update(self.player, self.dt)

        # Update the player
        self.player.update(self.level_manager.tile_rects, self.dt)


    def draw(self):
        # Fill the background
        self.display.fill((0, 0, 0))

        # Draw the background
        self.level_manager.draw_background(self.scroll, self.display)

        # Draw the triggers
        self.level_manager.draw_triggers(self.scroll, self.display)




        # Draw the entities
        self.level_manager.draw_entities(self.scroll, self.display)

        # Draw the tiles
        self.level_manager.draw_tiles(self.scroll, self.TILE_SIZE, self.display)

        # Draw player
        self.player.draw(self.display, self.scroll)

        # Scale up the display to the screen size, then draw it
        self.screen.blit(pg.transform.scale(self.display, self.WINDOW_SIZE), (0, 0))

        # Draw the UI on top of the screen
        self.UI.draw(self.screen, self.player, self.dt, self.clock, self.level_manager)

        # Draw the entire diaplay at once
        pg.display.flip()
