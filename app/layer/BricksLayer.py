from pygame.math import Vector2

from .Layer import Layer


class BricksLayer(Layer):
    def __init__(self, cellSize, imageFile, gameState, bricks):
        super().__init__(cellSize, imageFile)
        self.gameState = gameState
        self.bricks = bricks

    def render(self, surface):
        for brick in self.bricks:
            self.renderTile(surface, brick.position, brick.tile)
