from typing import List, TYPE_CHECKING

from .Layer import Layer

if TYPE_CHECKING:
    from app.state import Bullet


class BulletsLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, bullets: List["Bullet"]):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.bullets = bullets

    def render(self, surface):
        for bullet in self.bullets:
            if bullet.status == "alive":
                self.renderTile(surface, bullet.position, bullet.tile)
