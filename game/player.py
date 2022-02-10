import pygame as pg
from .engine import Entity


class Player(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, WALK_ACC=0, FRIC=0):
        super().__init__(x, y, width, height, type, WALK_ACC, FRIC)

        self.set_static_image('assets/animations/player/idle/idle_0.png')
        self.animation_frames['idle'] = self.load_animation('assets/animations/player/idle',[10, 10, 10, 10])
        self.animation_frames['walk'] = self.load_animation('assets/animations/player/walk',[5, 5, 5, 5, 5, 5])
        self.animation_frames['run'] = self.load_animation('assets/animations/player/run',[5, 5, 5, 5, 5, 5])
        self.animation_frames['roll'] = self.load_animation('assets/animations/player/roll',[5, 5, 5, 5, 5, 5])
        self.animation_frames['attack_1'] = self.load_animation('assets/animations/player/attack_1',[10, 10, 6, 5, 5, 5])
        self.animation_frames['jump'] = self.load_animation('assets/animations/player/jump',[5, 5, 7, 7, 7, 7])
        self.animation_frames['hurt'] = self.load_animation('assets/animations/player/hurt',[5, 10, 5])

        # Player Stats
        self.health = 100
        self.DAMAGES = {'attack_1': 25}
        self.DAMAGE_COOLDOWN = 25  # How many frames you are invinciple for after taking damage




