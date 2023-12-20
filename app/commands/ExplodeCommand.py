import random
from typing import TYPE_CHECKING
from pygame.math import Vector2
from app.state.Powerup import Powerup
from .Command import Command

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
        unitsAtPosition = self.state.findUnitsAt(self.explosion.position)

        for unit in unitsAtPosition:
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
                POWERUP_CHANCE = 0.25
                if random.random() < POWERUP_CHANCE:
                    self.state.powerups.append(Powerup(self.state, brick.position))

        if self.explosion.isTimeToDelete():
            self.explosion.status = "destroyed"
