import pygame

from pygame.math import Vector2
from app.state import GameState
from app.ui.layer import ArrayLayer, UnitsLayer, Layer, BulletsLayer, ExplosionsLayer
from app.state.commands import (
    MoveCommand,
    ShootCommand,
    MoveBulletCommand,
    DeleteDestroyedCommand,
    ExplodeCommand,
)


class UserInterface:
    def __init__(self, gameState: GameState):
        pygame.init()
        self.gameState = gameState
        self.layers = [
            ArrayLayer(
                self, "app/ui/sprites1.png", self.gameState, self.gameState.ground
            ),
            ArrayLayer(
                self, "app/ui/sprites1.png", self.gameState, self.gameState.walls
            ),
            UnitsLayer(
                self, "app/ui/sprites1.png", self.gameState, self.gameState.units
            ),
            BulletsLayer(
                self, "app/ui/sprites1.png", self.gameState, self.gameState.bullets
            ),
            ExplosionsLayer(
                self, "app/ui/explosions.png", self.gameState, self.gameState.explosions
            ),
        ]
        self.commands = []
        self.playerUnit = self.gameState.units[0]

        self.cellSize = Vector2(32, 32)

        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption(
            "Discover Python & Patterns - https://www.patternsgameprog.com"
        )
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        self.clock = pygame.time.Clock()
        self.running = True

    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def render(self):
        self.window.fill((0, 0, 0))

        for layer in self.layers:
            self.renderLayer(layer)

        pygame.display.update()

    def renderLayer(self, layer: Layer):
        layer.render(self.window)

    def processInput(self):
        moveVector = Vector2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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

    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()

        # Check game over
        if self.playerUnit.status != "alive":
            self.running = False
            print("GAME OVER")
