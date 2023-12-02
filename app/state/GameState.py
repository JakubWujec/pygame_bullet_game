from pygame.math import Vector2


class GameState:
    def __init__(self) -> None:
        self.tankPos = Vector2(8, 8)
        self.worldSize = Vector2(16, 16)
        self.blocksPos = [Vector2(9, 9), Vector2(10, 10)]

    def update(self, moveTankCommand: Vector2):
        newTankPos = self.tankPos + moveTankCommand

        if self.isPositionInsideWorld(newTankPos) and not self.isBlockAt(newTankPos):
            self.tankPos = newTankPos

    def isBlockAt(self, pos: Vector2):
        return pos in self.blocksPos

    def isPositionInsideWorld(self, pos: Vector2):
        return (
            pos.x >= 0
            and pos.x < self.worldSize.x
            and pos.y >= 0
            and pos.y < self.worldSize.y
        )
