from pygame.math import Vector2
from app.state.Orientation import Orientation
from .Command import Command


class MoveCommand(Command):
    def __init__(self, state, unit, moveVector: Vector2) -> None:
        super().__init__()
        self.state = state
        self.unit = unit
        self.moveVector = moveVector

    def run(self):
        # Update unit orientation
        if self.moveVector.x < 0:
            self.unit.orientation = Orientation.LEFT
        elif self.moveVector.x > 0:
            self.unit.orientation = Orientation.RIGHT
        if self.moveVector.y < 0:
            self.unit.orientation = Orientation.DOWN
        elif self.moveVector.y > 0:
            self.unit.orientation = Orientation.TOP

        # Compute new tank position
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
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # Don't allow bullets position
        for bullet in self.state.bullets:
            if newPos == bullet.position:
                return

        self.unit.position = newPos
