from pygame.math import Vector2
from app.state.Orientation import Orientation, orientationToVector, vectorToOrientation
from .Command import Command


class MoveCommand(Command):
    def __init__(self, state, unit, moveVector: Vector2) -> None:
        super().__init__()
        self.state = state
        self.unit = unit
        self.moveVector = moveVector

    def run(self):
        if vectorToOrientation(self.moveVector) != self.unit.orientation:
            self.unit.orientation = vectorToOrientation(self.moveVector)
            return

        # Update unit orientation
        if self.moveVector.x < 0:
            self.unit.orientation = Orientation.LEFT
        elif self.moveVector.x > 0:
            self.unit.orientation = Orientation.RIGHT
        if self.moveVector.y < 0:
            self.unit.orientation = Orientation.DOWN
        elif self.moveVector.y > 0:
            self.unit.orientation = Orientation.TOP

        # Compute new position
        newPos = self.unit.position + self.moveVector

        # Don't allow positions outside the world
        if (
            newPos.x < 0
            or newPos.x >= self.state.worldWidth
            or newPos.y < 0
            or newPos.y >= self.state.worldHeight
        ):
            return

        # Don't allow wall positions
        if self.state.isWallAt(newPos):
            return

        if self.state.isBrickAt(newPos):
            return

        if self.state.isPowerupAt(newPos):
            powerup = next(
                (
                    powerup
                    for powerup in self.state.powerups
                    if powerup.position == newPos
                ),
                None,
            )
            if powerup:
                powerup.apply(self.unit)

        for enemy in self.state.enemies:
            if newPos == enemy.position:
                self.unit.status = "destroyed"

        # Don't allow bullets position
        for bullet in self.state.bullets:
            if newPos == bullet.currentStopPosition():
                bullet.direction = orientationToVector(self.unit.orientation)
                return

        self.unit.position = newPos
