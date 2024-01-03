from pygame.math import Vector2
import math
from pygame import Rect
from app.state.Orientation import Orientation, orientationToVector, vectorToOrientation
from .Command import Command


class MoveCommand(Command):
    def __init__(self, state, unit, moveVector: Vector2) -> None:
        super().__init__()
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
        self.moveLength = 0.2

    def isVerticalMoveVector(self):
        return self.moveVector.x == 0 and self.moveVector.y != 0

    def needAligning(self):
        desiredPosition = (
            self.unit.closestIntegerPosition().elementwise() + self.moveVector
        )
        neededShiftVector = (
            self.unit.closestIntegerPosition().elementwise() - self.unit.position
        )
        if neededShiftVector.x == 0 and neededShiftVector.y == 0:
            return False

        # if not perpendicular then return False
        if not (neededShiftVector.normalize() * self.moveVector.normalize() == 0):
            return False

        if not self.state.isWalkableAt(
            self.unit.closestIntegerPosition()
        ) or not self.state.isWalkableAt(desiredPosition):
            return False
        if (0 < abs(neededShiftVector.x) <= 0.41 and neededShiftVector.y == 0) or (
            0 < abs(neededShiftVector.y) <= 0.41 and neededShiftVector.x == 0
        ):
            return True

        return False

    def alignPerpendicularly(self):
        return self.unit.closestIntegerPosition()

    def run(self):
        if vectorToOrientation(self.moveVector) != self.unit.orientation:
            self.unit.orientation = vectorToOrientation(self.moveVector)
            return

        # Update unit orientation
        if self.moveVector.x < 0 and self.unit.orientation != Orientation.LEFT:
            self.unit.orientation = Orientation.LEFT
            return
        elif self.moveVector.x > 0 and self.unit.orientation != Orientation.RIGHT:
            self.unit.orientation = Orientation.RIGHT
            return
        if self.moveVector.y < 0 and self.unit.orientation != Orientation.DOWN:
            self.unit.orientation = Orientation.DOWN
            return
        elif self.moveVector.y > 0 and self.unit.orientation != Orientation.TOP:
            self.unit.orientation = Orientation.TOP
            return

        # Compute new position
        newPos = round(
            self.unit.position
            + self.moveVector.elementwise() * Vector2(self.moveLength, self.moveLength),
            2,
        )

        if self.needAligning():
            newPos = self.unit.closestIntegerPosition()

        # nextStopPosition = self.unit.nextStopPosition()

        # Don't allow positions outside the world
        if (
            newPos.x < 0
            or newPos.x >= self.state.worldWidth
            or newPos.y < 0
            or newPos.y >= self.state.worldHeight
        ):
            return

        if self.state.isCollidingWithWallOrBrick(newPos):
            return

        # # Don't allow wall positions
        # if self.state.isWallAt(nextStopPosition):
        #     return

        # if self.state.isBrickAt(nextStopPosition):
        #     return

        # if self.state.isPowerupAt(nextStopPosition):
        #     powerup = next(
        #         (
        #             powerup
        #             for powerup in self.state.powerups
        #             if powerup.position == newPos
        #         ),
        #         None,
        #     )
        #     if powerup:
        #         powerup.apply(self.unit)

        # for enemy in self.state.enemies:
        #     if nextStopPosition == enemy.position:
        #         self.unit.status = "destroyed"

        # # Push bullet
        # for bullet in self.state.bullets:
        #     if nextStopPosition == bullet.currentStopPosition():
        #         bullet.direction = orientationToVector(self.unit.orientation)
        #         return
        self.unit.position = newPos
