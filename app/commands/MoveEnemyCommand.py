from pygame.math import Vector2
from app.state.Orientation import Orientation, orientationToVector, vectorToOrientation
from .Command import Command


class MoveEnemyCommand(Command):
    def __init__(
        self,
        state,
        enemy,
    ) -> None:
        super().__init__()
        self.state = state
        self.enemy = enemy

    def run(self):
        if not self.enemy.isReadyToMove():
            self.enemy.moveDelay -= 1
            return

        moveVector = orientationToVector(self.enemy.orientation)

        # Compute new position
        newPos = self.enemy.position.elementwise() + moveVector

        if self.canMoveTo(newPos):
            self.enemy.moveTo(newPos)
        else:
            self.enemy.turnAround()

    def canMoveTo(self, newPos):
        # Don't allow positions outside the world
        if (
            newPos.x < 0
            or newPos.x >= self.state.worldWidth
            or newPos.y < 0
            or newPos.y >= self.state.worldHeight
        ):
            return False

        # Don't allow wall positions
        if self.state.isWallAt(newPos) or self.state.isBrickAt(newPos):
            return False

        # Don't allow bullets position
        for bullet in self.state.bullets:
            if newPos == bullet.currentStopPosition():
                return False

        return True
