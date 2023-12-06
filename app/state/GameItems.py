from pygame.math import Vector2
from app.state.Orientation import Orientation, orientationToVector


class GameItem:
    def __init__(self, state, position, tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0


class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.lastBulletEpoch = -100


class Bullet(GameItem):
    def __init__(self, state, unit):
        super().__init__(state, unit.position, Vector2(3, 4))
        self.unit = unit
        self.startPosition = unit.position
        self.direction = orientationToVector(self.unit.orientation)

    def isMoving(self):
        return self.direction.x != 0 or self.direction.y != 0
