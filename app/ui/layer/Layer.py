import pygame
from pygame import Rect
from pygame.math import Vector2


class Layer:
    def __init__(self, ui, imageFile):
        self.ui = ui
        self.texture = pygame.image.load(imageFile)

    def renderTile(self, surface, position, tile: Vector2):
        # Location on screen
        spritePoint = position.elementwise() * self.ui.cellSize

        # Texture
        texturePoint = tile.elementwise() * self.ui.cellSize
        textureRect = Rect(
            int(texturePoint.x),
            int(texturePoint.y),
            self.ui.cellWidth,
            self.ui.cellHeight,
        )

        # Draw
        surface.blit(self.texture, spritePoint, textureRect)

    def render(self, surface):
        raise NotImplementedError()
