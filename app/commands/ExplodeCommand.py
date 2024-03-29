import random
from typing import TYPE_CHECKING, List

from app.commands import Command
from app.state.Powerup import PowerupFactory

if TYPE_CHECKING:
    from app.state import Explosion, Brick, GameState


class ExplodeCommand(Command):
    POWERUP_CHANCE = 1

    def __init__(self, state: "GameState", explosion: "Explosion") -> None:
        super().__init__()
        self.state = state
        self.explosion = explosion

    def run(self):
        self.destroyUnits()
        self.destroyEnemies()
        self.destroyBrick()

        if self.explosion.isTimeToDelete():
            self.explosion.status = "destroyed"

    def destroyUnits(self):
        collidingUnits = self.state.findCollidingUnits(self.explosion.position)
        for unit in collidingUnits:
            unit.status = "destroyed"

    def destroyEnemies(self):
        enemiesAtPosition = self.state.findEnemiesAt(self.explosion.position)
        for enemy in enemiesAtPosition:
            enemy.status = "destroyed"

    def destroyBrick(self):
        bricksToDestroy = self.findBricksToDestroy()
        for brick in bricksToDestroy:
            brick.status = "destroyed"
            if random.random() < ExplodeCommand.POWERUP_CHANCE:
                self.state.powerups.append(
                    PowerupFactory.createRandomPowerup(self.state, brick.position)
                )

    def findBricksToDestroy(self) -> List["Brick"]:
        return [
            brick
            for brick in self.state.bricks
            if brick.position
            == self.state.closestIntegerPosition(self.explosion.position)
        ]
