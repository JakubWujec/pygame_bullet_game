from pygame.math import Vector2
from app.state.units import Unit


class GameState:
    def __init__(self) -> None:
        self.worldSize = Vector2(16, 16)
        self.ground = [[Vector2(2, 26)] * 16 for x in range(16)]
        self.walls = [[None] * 16 for x in range(16)]
        self.units: [Unit] = [
            Unit(self, Vector2(8, 8), Vector2(13, 1)),
            Unit(self, Vector2(9, 9), Vector2(7, 26)),
            Unit(self, Vector2(10, 10), Vector2(7, 26)),
        ]

        for x in range(1, 16, 2):
            for y in range(1, 16, 2):
                self.walls[x][y] = Vector2(4, 26)

    @property
    def worldWidth(self):
        return int(self.worldSize.x)

    @property
    def worldHeight(self):
        return int(self.worldSize.y)
