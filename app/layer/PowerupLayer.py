from pygame.math import Vector2

from .Layer import Layer


class PowerupLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, powerups):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.powerups = powerups

    def render(self, surface):
        for powerup in self.powerups:
            self.renderTile(surface, powerup.position, powerup.tile)
