import pygame
from pygame import Rect
from pygame.math import Vector2
from app.state.Orientation import Orientation


class Layer:
    def __init__(self, ui, imageFile):
        self.ui = ui
        self.texture = pygame.image.load(imageFile)

    def renderTile(self, surface, position, tile: Vector2, angle=None):
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
        if angle is None:
            surface.blit(self.texture, spritePoint, textureRect)
        else:
            # Extract the tile in a surface
            textureTile = pygame.Surface(
                (self.ui.cellWidth, self.ui.cellHeight), pygame.SRCALPHA
            )
            textureTile.blit(self.texture, (0, 0), textureRect)
            # Rotate the surface with the tile
            rotatedTile = pygame.transform.rotate(textureTile, angle)
            # Compute the new coordinate on the screen, knowing that we rotate around the center of the tile
            spritePoint.x -= (rotatedTile.get_width() - textureTile.get_width()) // 2
            spritePoint.y -= (rotatedTile.get_height() - textureTile.get_height()) // 2
            # Render the rotatedTile
            surface.blit(rotatedTile, spritePoint)

    def render(self, surface):
        raise NotImplementedError()
