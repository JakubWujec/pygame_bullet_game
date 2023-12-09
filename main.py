import pygame


from app.mode import MenuGameMode, GameModeObserver


class Game(GameModeObserver):
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Bomberman")
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        # modes
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)

        # loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def quitRequested(self):
        self.running = False

    def run(self):
        while self.running:
            self.overlayGameMode.processInput()
            self.overlayGameMode.update()
            self.overlayGameMode.render(self.window)
            self.clock.tick(60)


game = Game()
game.run()
