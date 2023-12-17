from .GameItem import GameItem
from pygame.math import Vector2


class Explosion(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(6, 4))
        self.epoch = self.state.epoch
        self.center = position
        self.range = 2
        self.frameIndex = 0
        self.timeToLive = 100

    def isTimeToDelete(self):
        return self.state.epoch >= (self.epoch + self.timeToLive)
