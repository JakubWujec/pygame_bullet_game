from pygame.math import Vector2
from app.state.units import Unit, Block, Tank


class GameState:
    def __init__(self) -> None:
        self.worldSize = Vector2(16, 16)
        self.units: [Unit] = [
            Tank(self, Vector2(8, 8), Vector2(13, 1)),
            Block(self, Vector2(9, 9), Vector2(7, 26)),
            Block(self, Vector2(10, 10), Vector2(7, 26)),
        ]

    def update(self, moveVector: Vector2):
        for unit in self.units:
            unit.move(moveVector)

    def isPositionInsideWorld(self, pos: Vector2):
        return (
            pos.x >= 0
            and pos.x < self.worldSize.x
            and pos.y >= 0
            and pos.y < self.worldSize.y
        )
