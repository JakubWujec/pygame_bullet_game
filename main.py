import pygame

from app.mode import GameModeObserver, PlayGameMode, MenuGameMode, MessageGameMode
from app.commands import LoadLevelCommand


class UserInterface(GameModeObserver):
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((672, 672))
        pygame.display.set_caption("Bomberman")
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        # modes
        self.playGameMode = None

        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)

        self.currentActiveMode = "Overlay"

        # loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def quitRequested(self):
        self.running = False

    def gameLost(self):
        self.overlayGameMode = MessageGameMode("YOU LOST")
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = "Overlay"

    def loadLevelRequested(self, fileName):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode()
            self.playGameMode.addObserver(self)
        self.playGameMode.commands.append(LoadLevelCommand(self.playGameMode, fileName))
        try:
            self.playGameMode.update()
            self.currentActiveMode = "Play"
        except Exception as ex:
            print(ex)
            self.playGameMode = None
            # self.showMessage("Level loading failed :-(")

    def showMenuRequested(self):
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = "Overlay"

    def showGameRequested(self):
        if self.playGameMode is not None:
            self.currentActiveMode = "Play"

    def resizeRequested(self, windowSize):
        self.window = pygame.display.set_mode((int(windowSize.x), int(windowSize.y)))

    def run(self):
        while self.running:
            if self.currentActiveMode == "Overlay":
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            elif self.playGameMode is not None:
                self.playGameMode.processInput()
                try:
                    self.playGameMode.update()
                except Exception as ex:
                    print(ex)
                    self.playGameMode = None
                    # self.showMessage("Error during the game update...")

            if self.playGameMode is not None:
                self.playGameMode.render(self.window)
            else:
                self.window.fill((0, 0, 0))

            if self.currentActiveMode == "Overlay":
                darkSurface = pygame.Surface(
                    self.window.get_size(), flags=pygame.SRCALPHA
                )
                pygame.draw.rect(darkSurface, (0, 0, 0, 150), darkSurface.get_rect())
                self.window.blit(darkSurface, (0, 0))
                self.overlayGameMode.render(self.window)

            pygame.display.update()
            self.clock.tick(60)


ui = UserInterface()
ui.run()
