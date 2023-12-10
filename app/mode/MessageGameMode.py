import pygame

from .GameMode import GameMode


class MessageGameMode(GameMode):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message
        self.font = pygame.font.Font(None, 16)
        self.textColor = (34, 139, 34)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyQuitRequested()
                    break
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    self.notifyShowMenuRequested()

    def update(self):
        pass

    def render(self, window):
        window.fill((0, 0, 0))

        # Render the text
        textSurface = self.font.render(self.message, True, self.textColor)

        # Get the rectangle containing the text surface
        textRect = textSurface.get_rect()

        # Center the text on the screen
        textRect.center = (512 // 2, 512 // 2)

        # Blit the text surface onto the main surface
        window.blit(textSurface, textRect)

        pygame.display.update()
