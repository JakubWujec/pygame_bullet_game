from typing import Optional
import pygame

from pygame.math import Vector2
from pygame import Rect
from app.state.units import Unit
from app.state import GameState
from app.ui.layer import ArrayLayer, UnitsLayer, Layer


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
        ]

        self.cellSize = Vector2(32, 32)

        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))
        pygame.display.set_caption(
            "Discover Python & Patterns - https://www.patternsgameprog.com"
        )
        # pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommand = Vector2(0, 0)

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
