from .GameItem import GameItem
from pygame.math import Vector2


class Explosion(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(15, 30))
        self.epoch = self.state.epoch
        self.center = position
        self.range = 2
        self.frameIndex = 0
        self.ttl = 300

    def isTimeToDelete(self):
        return self.state.epoch >= (self.epoch + self.ttl)
