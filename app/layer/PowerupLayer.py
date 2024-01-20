from typing import TYPE_CHECKING, List
from pygame.math import Vector2
from .Layer import Layer

if TYPE_CHECKING:
    from app.state import Powerup, GameState


class PowerupLayer(Layer):
    def __init__(
        self,
        cellSize: Vector2,
        imageFile: str,
        gameState: "GameState",
        powerups: List["Powerup"],
    ):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.powerups = powerups

    def render(self, surface):
        for powerup in self.powerups:
            self.renderTile(surface, powerup.position, powerup.tile)
