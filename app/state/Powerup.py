from .GameItem import GameItem
from pygame.math import Vector2


class Powerup(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(0, 15))
        self.timeToLive = 200

    def apply(self, unit):
        unit.bulletLimit += 1
        self.status = "destroyed"
