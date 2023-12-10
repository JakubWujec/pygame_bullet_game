from pygame.math import Vector2

from .Layer import Layer


class ExplosionsLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, explosions):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.explosions = explosions

    def render(self, surface):
        for explosion in self.explosions:
            self.renderTile(surface, explosion.position, explosion.tile)
