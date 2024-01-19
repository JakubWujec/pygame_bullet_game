import math
from typing import TYPE_CHECKING, List

from pygame.math import Vector2

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
                self.renderTile(surface, bullet.position, self.getBulletTile(bullet))

    def getBulletTile(self, bullet: "Bullet"):
        frames = 5
        bulletTimeToLive = bullet.timeToLive
        timePassed = self.gameState.epoch - bullet.epoch
        frameIndex = (timePassed / bulletTimeToLive) * frames
        frameIndex = math.floor(frameIndex)
        return Vector2(frameIndex, 0)
