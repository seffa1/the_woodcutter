import pygame as pg
import sys, time
from .utils import draw_text
from .engine import Entity
from .entity_manager import Entity_Manager
from .player import Player

# TODO
#   Rolling, attacking, jumping, hanging,
#   Batch Rendering of ground for less collisions checks
#   Only checking collisions on tiles close to player
#   Move level creation over to other classes

vec = pg.math.Vector2

class Game:
    def __init__(self, screen, clock, display, WINDOW_SIZE, SCALE_FACTOR):
        # Game setup
        self.screen = screen
        self.clock = clock
        self.display = display
        self.WINDOW_SIZE = WINDOW_SIZE
        self.SCALE_FACTOR = SCALE_FACTOR
        self.TILE_SIZE = 24
        self.width, self.height = self.screen.get_size()
        self.last_time = time.time()  # For frame rate independence
        self.dt = 0

        # Camera Scroll
        self.true_scroll = [0, 0]  # The scroll as a percise float
        self.scroll = [0, 0]  # The scroll rounded to an int
        self.OFFSET_X = WINDOW_SIZE[0] / SCALE_FACTOR / 2
        self.OFFSET_Y = WINDOW_SIZE[1] / SCALE_FACTOR / 3 * 2

        # Managers
        self.entity_manager = Entity_Manager()

        # Player
        self.player = Player(100, 100, 30, 35, 'player', WALK_ACC=.3, FRIC=-.15)
        self.player.set_static_image('assets/animations/player/idle/idle_0.png')
        self.player.animation_frames['idle'] = self.player.load_animation('assets/animations/player/idle', [10, 10, 10, 10])
        self.player.animation_frames['walk'] = self.player.load_animation('assets/animations/player/walk', [5, 5, 5, 5, 5, 5])
        self.player.animation_frames['run'] = self.player.load_animation('assets/animations/player/run', [5, 5, 5, 5, 5, 5])
        self.player.animation_frames['roll'] = self.player.load_animation('assets/animations/player/roll', [5, 5, 5, 5, 5, 5])
        self.player.animation_frames['attack_1'] = self.player.load_animation('assets/animations/player/attack_1', [5, 5, 5, 5, 5, 5])

        # Temporary stuff to be moved elsewhere
        self.background_images = []
        path = 'assets/images/backgrounds/rocks_1'
        paralax_dif = .02
        paralax = 0
        for i in range(0, 7):
            img_path = path + '/' + str(i + 1) + '.png'
            image = pg.image.load(img_path).convert_alpha()
            scaled_image = pg.transform.scale(image, (self.display.get_width()*1.5, self.display.get_height()*1.5))
            self.background_images.append([scaled_image, paralax])
            paralax += paralax_dif
        self.grass_tile_top = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_02.png').convert_alpha(), (self.TILE_SIZE, self.TILE_SIZE))
        self.dirt_tile = pg.transform.scale(pg.image.load('assets/images/tiles/Tile_11.png').convert_alpha() ,(self.TILE_SIZE, self.TILE_SIZE))
        self.tile_rects = []

    # Also temporary to be moved elsewheere
    def load_map(self, path: str):
        with open (path, 'r') as file:
            data = file.read()
            data = data.split('\n')
            game_map = []
            for row in data:
                game_map.append(list(row))
            return game_map

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)

            # Frame rate independence check
            # Finds how many seconds have passed since the last frame
            # If we are at 60 fps, dt will be 1/60th of a second
            self.dt = time.time() - self.last_time
            # Multiply it by 60 so if we are at 60 fps, dt is 1
            # If we ran at 30 fps, dt would be 2/60th * 60 = 2
            # So everything that moves get multiplied by 2
            self.dt *= 60
            self.last_time = time.time()

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            mods = pg.key.get_mods()
            if mods & pg.KMOD_SHIFT:
                self.player.run = True
            else:
                self.player.run = False


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                if event.key == pg.K_d:
                    self.player.walk_right = True
                if event.key == pg.K_a:
                    self.player.walk_left = True
                if event.key == pg.K_w and not self.player.roll:  # Cant jump while rolling
                    self.player.jump()
                if event.key == pg.K_SPACE and not self.player.roll and self.player.collision_types['bottom']:  # Cant roll unless on the ground
                    self.player.roll = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    self.player.walk_right = False
                if event.key == pg.K_a:
                    self.player.walk_left = False



    def update(self):
        # Scroll
        # Sets the "cameras" position. The divisor adds the lagging behind, smoothing effect
        self.true_scroll[0] += (self.player.rect.x - self.true_scroll[0] - self.OFFSET_X) / 20
        self.true_scroll[1] += (self.player.rect.y - self.true_scroll[1] - self.OFFSET_Y) / 20
        scroll = self.true_scroll.copy()
        # Rounds the float to an int for the drawings not to get choppy
        self.scroll[0] = int(scroll[0])
        self.scroll[1] = int(scroll[1])

        # Update the player
        self.player.update(self.tile_rects, self.dt)

    def draw(self):
        # Fill the background
        self.display.fill((0, 0, 0))

        # Temp background
        for image in self.background_images:
            self.display.blit(image[0], (-image[1]*self.scroll[0], -image[1]*self.scroll[1] - image[0].get_height()/3))

        # Temp tile rendering
        self.tile_rects = []
        y = 0
        for layer in self.load_map('game/maps/1.txt'):
            x = 0
            for tile in layer:
                if tile == '1':
                    self.display.blit(self.dirt_tile, (x * self.TILE_SIZE - self.scroll[0], y * self.TILE_SIZE - self.scroll[1]))
                if tile == '2':
                    self.display.blit(self.grass_tile_top, (x * self.TILE_SIZE - self.scroll[0], y * self.TILE_SIZE - self.scroll[1]))
                    self.tile_rects.append(pg.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1

        # Draw player
        self.player.draw(self.display, self.scroll)

        # Draw the UI
        self.screen.blit(pg.transform.scale(self.display, self.WINDOW_SIZE), (0, 0))


        draw_text(self.screen, f'fps: {round(self.clock.get_fps())}', 25, (255, 0, 0), (3, 3))
        draw_text(self.screen, f'player pos: {self.player.pos}', 25, (255, 0, 0), (3, 23))
        draw_text(self.screen, f'p_rect pos: {self.player.rect.topleft}', 25, (255, 0, 0), (3, 43))
        draw_text(self.screen, f'vel pos: {self.player.vel}', 25, (255, 0, 0), (3, 63))
        draw_text(self.screen, f'action: {self.player.action}', 25, (255, 0, 0), (3, 83))

        pg.display.flip()
