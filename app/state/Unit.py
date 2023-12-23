from .GameItem import GameItem


class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state, position, tile)
        self.lastBulletEpoch = -1 * self.state.bulletDelay
        self.bulletLimit = 1
        self.bulletRange = 1

    def canShoot(self):
        if self.state.epoch - self.lastBulletEpoch < self.state.bulletDelay:
            return False

        unitBullets = sum(1 for bullet in self.state.bullets if bullet.unit == self)

        return unitBullets < self.bulletLimit
