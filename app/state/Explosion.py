from pygame.math import Vector2
from .GameItem import GameItem


class Explosion(GameItem):
    def __init__(self, state, position: Vector2, tile=Vector2(6, 4)):
        super().__init__(state, position, tile)
        self.epoch = self.state.epoch
        self.center = position
        self.timeToLive: int = 100

    def isTimeToDelete(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)
