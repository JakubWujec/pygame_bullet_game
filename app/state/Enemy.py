from typing import TYPE_CHECKING

from pygame.math import Vector2

from .GameItem import GameItem

if TYPE_CHECKING:
    from app.state import GameState


class Enemy(GameItem):
    def __init__(self, state: "GameState", position: Vector2):
        super().__init__(state, position, Vector2(11, 1))
        self.moveDelay: int = 100
        self.lastMoveEpoch: int = 0

    def isReadyToMove(self) -> bool:
        return self.state.epoch >= self.lastMoveEpoch + self.moveDelay
