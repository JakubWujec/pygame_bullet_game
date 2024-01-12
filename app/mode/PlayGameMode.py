from typing import TYPE_CHECKING

import pygame
from pygame.math import Vector2

from app.commands import (
    DeleteDestroyedCommand,
    ExplodeCommand,
    MoveBulletCommand,
    MoveCommand,
    MoveEnemyCommand,
    ShootCommand,
    MakeBulletExplodeCommand,
)
from app.layer import (
    ArrayLayer,
    BricksLayer,
    BulletsLayer,
    EnemiesLayer,
    ExplosionsLayer,
    PowerupLayer,
    UnitsLayer,
)
from app.state.GameState import GameState

from .GameMode import GameMode

if TYPE_CHECKING:
    from app.state.Powerup import Powerup


class PlayGameMode(GameMode):
    def __init__(self) -> None:
        super().__init__()
        self.gameState = GameState()
        self.cellSize = Vector2(32, 32)
        self.layers = [
            ArrayLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.ground,
            ),
            ArrayLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.walls,
            ),
            BricksLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.bricks,
            ),
            UnitsLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.units,
            ),
            EnemiesLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.enemies,
            ),
            PowerupLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.powerups,
            ),
            BulletsLayer(
                self.cellSize,
                "app/assets/sprites1.png",
                self.gameState,
                self.gameState.bullets,
            ),
            ExplosionsLayer(
                self.cellSize,
                "app/assets/explosions.png",
                self.gameState,
                self.gameState.explosions,
            ),
        ]
        self.commands = []
        self.playerUnit = None
        self.gameOver = False

    def processInput(self):
        pygame.time.delay(30)
        moveVector = Vector2()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    self.notifyQuitRequested()
                    break
                elif event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                    break

        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_RIGHT]:
            moveVector = Vector2(1, 0)

        if pressedKeys[pygame.K_LEFT]:
            moveVector = Vector2(-1, 0)

        if pressedKeys[pygame.K_DOWN]:
            moveVector = Vector2(0, 1)

        if pressedKeys[pygame.K_UP]:
            moveVector = Vector2(0, -1)

        if pressedKeys[pygame.K_SPACE]:
            shootCommand = ShootCommand(self.gameState, self.playerUnit)
            self.commands.append(shootCommand)

        # player movement
        if moveVector.x != 0 or moveVector.y != 0:
            command = MoveCommand(self.gameState, self.playerUnit, moveVector)
            self.commands.append(command)

        # Bullets automatic movement
        for bullet in self.gameState.bullets:
            self.commands.append(MoveBulletCommand(self.gameState, bullet))

        # Enemies movement
        for enemy in self.gameState.enemies:
            self.commands.append(MoveEnemyCommand(self.gameState, enemy))

        # Handle bullet to explosion transition
        for bullet in self.gameState.bullets:
            if bullet.isTimeToExplode():
                self.commands.append(MakeBulletExplodeCommand(self.gameState, bullet))

        # Handle explosions
        for explosion in self.gameState.explosions:
            self.commands.append(ExplodeCommand(self.gameState, explosion))

        # Delete any destroyed bullet
        self.commands.append(DeleteDestroyedCommand(self.gameState.bullets))

        # Delete any destroyed explosions
        self.commands.append(DeleteDestroyedCommand(self.gameState.explosions))

        # Delete any destroyed powerups
        for powerup in self.gameState.powerups:
            if powerup.isTimeToDelete():
                powerup.status = "destroyed"
        self.commands.append(DeleteDestroyedCommand(self.gameState.powerups))

        # Delete any destroyed enemies
        self.commands.append(DeleteDestroyedCommand(self.gameState.enemies))

        # Delete any destroyed bricks
        self.commands.append(DeleteDestroyedCommand(self.gameState.bricks))

    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1

        # Check game over
        if self.playerUnit.status != "alive":
            self.gameOver = True
            self.notifyGameLost()

        if len(self.gameState.enemies) == 0:
            self.gameOver = True
            self.notifyGameWon()

    def render(self, window):
        for layer in self.layers:
            layer.render(window)
