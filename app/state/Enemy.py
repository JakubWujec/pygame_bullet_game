from typing import TYPE_CHECKING

from pygame.math import Vector2

from .GameItem import GameItem
from .Orientation import vectorToOrientation, orientationToVector

if TYPE_CHECKING:
    from app.state import GameState


class Enemy(GameItem):
    def __init__(self, state: "GameState", position):
        super().__init__(state, position, Vector2(11, 1))
        self.moveDelay = 100
        self.lastMoveEpoch = 0

    def isReadyToMove(self):
        return self.lastMoveEpoch + self.moveDelay >= self.state.epoch

    def moveTo(self, newPosition):
        self.position = newPosition
        self.lastMoveEpoch = self.state.epoch

    def turnAround(self):
        moveVector = orientationToVector(self.orientation)
        self.orientation = vectorToOrientation(
            moveVector.elementwise() * Vector2(-1, -1)
        )
