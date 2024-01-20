from typing import TYPE_CHECKING
from pygame.math import Vector2

if TYPE_CHECKING:
    from app.state import GameState


class GameItem:
    def __init__(self, state: "GameState", position: Vector2, tile: Vector2):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0

    def collideWith(self, position: Vector2):
        return (
            abs(self.position.x - position.x) < 1
            and abs(self.position.y - position.y) < 1
        )
