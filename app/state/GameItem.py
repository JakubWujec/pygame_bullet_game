from pygame.rect import Rect
from pygame.math import Vector2


class GameItem:
    def __init__(self, state, position, tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0

    def collideWith(self, position: Vector2):
        rect1 = Rect(position.x * 10, position.y * 10, 10, 10)
        rect2 = Rect(self.position.x * 10, self.position.y * 10, 10, 10)

        return rect1.colliderect(rect2)
