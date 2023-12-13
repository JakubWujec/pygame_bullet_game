from .GameItem import GameItem
from pygame.math import Vector2


class Brick(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(4, 1))
