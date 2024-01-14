import unittest
from unittest.mock import Mock
from app.state import GameState, Unit, Orientation
from app.commands import (
    ShootCommand,
)
from pygame.math import Vector2


class TestShootCommand(unittest.TestCase):
    def setUp(self):
        self.mockState = Mock(spec=GameState)
        self.mockUnit = Mock(spec=Unit)
        self.shootCommand = ShootCommand(self.mockState, self.mockUnit)

    def testCanUnitShootAlive(self):
        self.mockUnit.status = "alive"
        self.mockUnit.canShoot.return_value = True
        self.assertTrue(self.shootCommand.canUnitShoot())

    def testCanUnitShootDestroyed(self):
        self.mockUnit.status = "destroyed"
        self.mockUnit.canShoot.return_value = True
        self.assertFalse(self.shootCommand.canUnitShoot())

    def testCanUnitShootCannotShoot(self):
        self.mockUnit.status = "alive"
        self.mockUnit.canShoot.return_value = False
        self.assertFalse(self.shootCommand.canUnitShoot())

    def testCalculateBulletStartPosition(self):
        # Mock the orientation
        self.mockUnit.orientation = Orientation.RIGHT
        self.mockUnit.closestIntegerPosition.return_value = Vector2(1, 1)

        result = self.shootCommand.calculateBulletStartPosition()

        expectedResult = Vector2(1, 1)
        self.assertEqual(result, expectedResult)


class TestShootCommandMultipleBullets(unittest.TestCase):
    def setUp(self):
        self.state = GameState(Vector2(2, 2))
        self.unit = Unit(self.state, Vector2(0, 0), Vector2(1, 1))
        self.shootCommand = ShootCommand(self.state, self.unit)

    def testCanPutOneBulletInOnePosition(self):
        # ignore unit reload time
        self.shootCommand.canUnitShoot = Mock(return_Value=True)
        self.assertTrue(len(self.state.bullets) == 0)
        self.shootCommand.run()
        self.assertTrue(len(self.state.bullets) == 1)

    def testCannotPutMutlipleBulletInOnePosition(self):
        # ignore unit reload time
        self.shootCommand.canUnitShoot = Mock(return_Value=True)

        self.assertTrue(len(self.state.bullets) == 0)
        self.shootCommand.run()
        self.shootCommand.run()
        self.assertTrue(len(self.state.bullets) == 1)
