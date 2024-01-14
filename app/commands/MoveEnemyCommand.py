from typing import TYPE_CHECKING

from pygame.math import Vector2

from app.state.Orientation import orientationToVector

from .Command import Command

if TYPE_CHECKING:
    from app.state import GameState


class MoveEnemyCommand(Command):
    def __init__(
        self,
        state: "GameState",
        enemy,
    ) -> None:
        super().__init__()
        self.state = state
        self.enemy = enemy

    def run(self):
        if not self.enemy.isReadyToMove():
            return

        moveVector = orientationToVector(self.enemy.orientation)

        # Compute new position
        newPos = self.enemy.position.elementwise() + moveVector

        if self.canMoveTo(newPos):
            self.enemy.moveTo(newPos)
            for unit in self.state.units:
                if newPos == unit.position:
                    unit.status = "destroyed"

        else:
            self.enemy.turnAround()

    def canMoveTo(self, newPos):
        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            return False

        # Don't allow wall / bricks positions
        if self.state.isWallAt(newPos) or self.state.isBrickAt(newPos):
            return False

        # Don't allow bullets position
        if any(newPos == bullet.currentStopPosition() for bullet in self.state.bullets):
            return False

        # Don't allow positions in explosions
        if any(newPos == explosion.position for explosion in self.state.explosions):
            return False

        return True
