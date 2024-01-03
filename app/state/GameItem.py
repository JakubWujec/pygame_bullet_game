from pygame.rect import Rect


class GameItem:
    def __init__(self, state, position, tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0

    def collideWith(self, gameItem):
        rect1 = Rect(gameItem.position.x, gameItem.position.y, 1, 1)
        rect2 = Rect(self.position.x, self.position.y, 1, 1)
        return rect1.colliderect(rect2)
