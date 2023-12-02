from typing import Optional

import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

from ui import Theme
from ui.mode import GameMode


class UserInterface:
    def __init__(self, theme: Theme):
        # Create window with default resolution

        pygame.init()

        self.__window = pygame.display.set_mode(
            (1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE
        )
        pygame.display.set_caption(
            "2D Medieval Strategy Game with Python, http://www.patternsgameprog.com"
        )
        pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))

        # Rendering properties
        self.__theme = theme
        self.__rescaledX = 0
        self.__rescaledY = 0
        self.__rescaledScaleX = 1.0
        self.__rescaledScaleY = 1.0
        self.__renderWidth = self.__window.get_width()
        self.__renderHeight = self.__window.get_height()

        # Other
        self.__gameMode: Optional[GameMode] = None
        self.__running = True
        self.__clock = pygame.time.Clock()

    @property
    def theme(self) -> Theme:
        return self.__theme

    def setGameMode(self, gameMode: GameMode):
        self.__gameMode = gameMode

    def setRenderSize(self, renderWidth: int, renderHeight: int):
        self.__renderWidth = renderWidth
        self.__renderHeight = renderHeight

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

    def update(self):
        if self.__gameMode is not None:
            self.__gameMode.update()

    def render(self):
        # Render world in a surface
        renderSurface = Surface((self.__renderWidth, self.__renderHeight))
        if self.__gameMode is not None:
            self.__gameMode.render(renderSurface)

        # Scale rendering to window size
        windowWidth, windowHeight = self.__window.get_size()
        renderRatio = self.__renderWidth / self.__renderHeight
        windowRatio = windowWidth / windowHeight
        if windowRatio <= renderRatio:
            rescaledSurfaceWidth = windowWidth
            rescaledSurfaceHeight = int(windowWidth / renderRatio)
            self.__rescaledX = 0
            self.__rescaledY = (windowHeight - rescaledSurfaceHeight) // 2
        else:
            rescaledSurfaceWidth = int(windowHeight * renderRatio)
            rescaledSurfaceHeight = windowHeight
            self.__rescaledX = (windowWidth - rescaledSurfaceWidth) // 2
            self.__rescaledY = 0

        # Scale the rendering to the window/screen size
        rescaledSurface = pygame.transform.scale(
            renderSurface, (rescaledSurfaceWidth, rescaledSurfaceHeight)
        )
        self.__rescaledScaleX = rescaledSurface.get_width() / renderSurface.get_width()
        self.__rescaledScaleY = (
            rescaledSurface.get_height() / renderSurface.get_height()
        )
        self.__window.blit(rescaledSurface, (self.__rescaledX, self.__rescaledY))

    def run(self):
        # Main game loop
        while self.__running:
            self.processInput()
            self.update()
            self.render()

            pygame.display.update()
            self.__clock.tick(30)

    def quit(self):
        pygame.quit()
