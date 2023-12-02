from pygame.math import Vector2


class GameState:
    def __init__(self) -> None:
        self.tankPos = Vector2(8, 8)
        self.worldSize = Vector2(16, 16)

    def update(self, moveTankCommand):
        self.tankPos += moveTankCommand

        if self.tankPos.x < 0:
            self.tankPos.x = 0
        elif self.tankPos.x >= self.worldSize.x:
            self.tankPos.x = self.worldSize.x - 1

        if self.tankPos.y < 0:
            self.tankPos.y = 0
        elif self.tankPos.y >= self.worldSize.y:
            self.tankPos.y = self.worldSize.y - 1
