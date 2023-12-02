from typing import Optional
import pygame

from pygame.math import Vector2
from pygame import Rect
from app.state.units import Unit
from app.state import GameState


class UserInterface:
    def __init__(self, gameState: GameState):
        pygame.init()
        self.gameState = gameState

        self.cellSize = Vector2(32, 32)
        self.unitsTexture = pygame.image.load("app/ui/sprites1.png")

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

        for y in range(self.gameState.worldHeight):
            for x in range(self.gameState.worldWidth):
                self.renderGround(Vector2(x, y), self.gameState.ground[y][x])

        for unit in self.gameState.units:
            self.__renderUnit(unit)

        pygame.display.update()

    def renderGround(self, position, tile):
        # Location on screen
        spritePoint = position.elementwise() * self.cellSize

        # Texture
        texturePoint = tile.elementwise() * self.cellSize
        textureRect = Rect(
            int(texturePoint.x),
            int(texturePoint.y),
            self.cellWidth,
            self.cellHeight,
        )
        self.window.blit(self.unitsTexture, spritePoint, textureRect)

    def __renderUnit(self, unit: Unit):
        # location on screen
        spritePoint = unit.position.elementwise() * self.cellSize

        # Unit texture
        texturePoint = unit.tile.elementwise() * self.cellSize
        textureRect = Rect(
            int(texturePoint.x),
            int(texturePoint.y),
            self.cellWidth,
            self.cellHeight,
        )

        self.window.blit(self.unitsTexture, spritePoint, textureRect)
