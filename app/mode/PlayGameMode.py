import pygame
from pygame.math import Vector2
from app.state.GameState import GameState
from app.layer import ArrayLayer, BulletsLayer, ExplosionsLayer, UnitsLayer, BricksLayer
from app.commands import (
    MoveBulletCommand,
    MoveCommand,
    ShootCommand,
    ExplodeCommand,
    DeleteDestroyedCommand,
)
from .GameMode import GameMode


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
        moveVector = Vector2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                    break
                if event.key == pygame.K_RIGHT:
                    moveVector = Vector2(1, 0)
                elif event.key == pygame.K_LEFT:
                    moveVector = Vector2(-1, 0)
                elif event.key == pygame.K_DOWN:
                    moveVector = Vector2(0, 1)
                elif event.key == pygame.K_UP:
                    moveVector = Vector2(0, -1)
                elif event.key == pygame.K_SPACE:
                    shootCommand = ShootCommand(self.gameState, self.playerUnit)
                    self.commands.append(shootCommand)

        # player movement
        if moveVector.x != 0 or moveVector.y != 0:
            command = MoveCommand(self.gameState, self.playerUnit, moveVector)
            self.commands.append(command)

        # Bullets automatic movement
        for bullet in self.gameState.bullets:
            self.commands.append(MoveBulletCommand(self.gameState, bullet))

        # Handle explosions
        for explosion in self.gameState.explosions:
            self.commands.append(ExplodeCommand(self.gameState, explosion))

        # Delete any destroyed bullet
        self.commands.append(DeleteDestroyedCommand(self.gameState.bullets))

        # Delete any destroyed explosions
        self.commands.append(DeleteDestroyedCommand(self.gameState.explosions))

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

    def render(self, window):
        for layer in self.layers:
            layer.render(window)
