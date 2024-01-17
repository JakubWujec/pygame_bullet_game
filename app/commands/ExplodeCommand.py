import random
from typing import TYPE_CHECKING

from app.commands import Command
from app.state.Powerup import PowerupFactory

if TYPE_CHECKING:
    from app.state.Brick import Brick
    from app.state.GameState import GameState


class ExplodeCommand(Command):
    def __init__(self, state, explosion) -> None:
        super().__init__()
        self.state: GameState = state
        self.explosion = explosion

    def run(self):
        # if explosion touch unit destroy it
        collidingUnits = self.state.findCollidingUnits(self.explosion.position)
        for unit in collidingUnits:
            unit.status = "destroyed"

        enemiesAtPosition = self.state.findEnemiesAt(self.explosion.position)
        for enemy in enemiesAtPosition:
            enemy.status = "destroyed"

        if self.state.isBrickAt(self.explosion.position):
            brickToDestroy: list[Brick] = list(
                filter(
                    lambda brick: brick.position == self.explosion.position,
                    self.state.bricks,
                )
            )
            for brick in brickToDestroy:
                brick.status = "destroyed"
                POWERUP_CHANCE = 1
                if random.random() < POWERUP_CHANCE:
                    self.state.powerups.append(
                        PowerupFactory.createRandomPowerup(self.state, brick.position)
                    )

        if self.explosion.isTimeToDelete():
            self.explosion.status = "destroyed"
