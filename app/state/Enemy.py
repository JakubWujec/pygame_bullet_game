from pygame.math import Vector2

from .GameItem import GameItem


class Enemy(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(11, 1))
