from pygame.math import Vector2

from .GameItem import GameItem
from .Orientation import vectorToOrientation, orientationToVector


class Enemy(GameItem):
    def __init__(self, state, position):
        super().__init__(state, position, Vector2(11, 1))
        self.moveDelay = 100

    def isReadyToMove(self):
        return self.moveDelay <= 0

    def moveTo(self, newPosition):
        self.position = newPosition
        self.moveDelay = 100

    def turnAround(self):
        moveVector = orientationToVector(self.orientation)
        self.orientation = vectorToOrientation(
            moveVector.elementwise() * Vector2(-1, -1)
        )
        self.moveDelay = 100
