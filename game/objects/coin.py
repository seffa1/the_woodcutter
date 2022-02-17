from game.engine import Entity
import pygame as pg


class Coin(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str = None, WALK_ACC=0, FRIC=0, rotate=None):
        super().__init__()