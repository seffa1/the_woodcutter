import pygame as pg
from .engine import Entity


class Player(Entity):
    def __init__(self, x: int, y: int, width: int, height: int, type: str=None, ACC=0, FRIC=0):
        super().__init__(x, y, width, height, type, ACC, FRIC)

