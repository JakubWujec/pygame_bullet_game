from .GameItem import GameItem


class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.lastBulletEpoch = -1 * self.state.bulletDelay
        self.bulletLimit = 2

    def canShoot(self):
        if self.state.epoch - self.lastBulletEpoch < self.state.bulletDelay:
            return False

        unitBullets = len(
            list(filter(lambda bullet: bullet.unit == self, self.state.bullets))
        )

        if unitBullets >= self.bulletLimit:
            return False

        return True
