from .GameItem import GameItem


class Powerup(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.timeToLive = 200

    def apply(self, unit):
        pass
