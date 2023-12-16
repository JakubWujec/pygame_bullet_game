from pygame.math import Vector2

from .Layer import Layer


class EnemiesLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, enemies):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.enemies = enemies

    def render(self, surface):
        for unit in self.enemies:
            self.renderTile(surface, unit.position, unit.tile, unit.orientation)
