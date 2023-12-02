from typing import Optional
import pygame

from pygame.math import Vector2
from pygame import Rect

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

    def render(self):
        self.window.fill((0, 0, 0))

        self.__drawBlocks()
        self.__drawTank()

        pygame.display.update()

    def __drawBlocks(self):
        for block in [self.gameState.block1, self.gameState.block2]:
            spritePoint = block.elementwise() * self.cellSize

            texturePoint = Vector2(7, 26).elementwise() * self.cellSize
            textureRect = Rect(
                int(texturePoint.x),
                int(texturePoint.y),
                int(self.cellSize.x),
                int(self.cellSize.y),
            )

            self.window.blit(self.unitsTexture, spritePoint, textureRect)

    def __drawTank(self):
        spritePoint = self.gameState.tankPos.elementwise() * self.cellSize

        texturePoint = Vector2(13, 1).elementwise() * self.cellSize
        textureRect = Rect(
            int(texturePoint.x),
            int(texturePoint.y),
            int(self.cellSize.x),
            int(self.cellSize.y),
        )

        self.window.blit(self.unitsTexture, spritePoint, textureRect)
