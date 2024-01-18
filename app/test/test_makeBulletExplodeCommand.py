import unittest
from unittest.mock import MagicMock
from pygame.math import Vector2
from app.state import Bullet, Explosion, GameState, Unit
from app.commands import (
    MakeBulletExplodeCommand,
)


class TestMakeBulletExplodeCommand(unittest.TestCase):
    def setUp(self):
        self.state = GameState(worldSize=Vector2(20, 20))
        self.unit = Unit(self.state, Vector2(1, 1), Vector2(1, 1))
        self.bullet = Bullet(self.state, self.unit, Vector2(10, 10))
        self.command = MakeBulletExplodeCommand(self.state, self.bullet)

    def test_commandDestroysBullet(self):
        # Ensure bullet status is set to "destroyed"
        self.assertEqual(self.bullet.status, "alive")
        self.command.run()
        self.assertEqual(self.bullet.status, "destroyed")

    def test_createCentralAtTheSamePositionAsBullet(self):
        # Ensure a central explosion is created with the correct tile
        self.assertEqual(len(self.state.explosions), 0)
        self.command.createCentralExplosion()
        self.assertEqual(len(self.state.explosions), 1)
        central_explosion = self.state.explosions[0]
        self.assertIsInstance(central_explosion, Explosion)
        self.assertEqual(central_explosion.position, self.bullet.position)

    def test_createDirectionalExplosionsWithRangeOne(self):
        # Ensure directional explosions are created based on bullet range
        self.bullet.bulletRange = 1
        self.assertEqual(len(self.state.explosions), 0)
        self.command.createDirectionalExplosions()
        self.assertEqual(len(self.state.explosions), 4)

    def test_createDirectionalExplosionsWithRangeTwo(self):
        # Ensure directional explosions are created based on bullet range
        state = GameState(worldSize=Vector2(20, 20))
        unit = Unit(state, Vector2(5, 5), Vector2(1, 1))
        unit.bulletRange = 2
        bullet = Bullet(state, unit, Vector2(10, 10))
        command = MakeBulletExplodeCommand(state, bullet)

        self.assertEqual(len(state.explosions), 0)
        command.createDirectionalExplosions()
        self.assertEqual(len(state.explosions), 8)
