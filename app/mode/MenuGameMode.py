import pygame

from .GameMode import GameMode


class MenuGameMode(GameMode):
    def __init__(self) -> None:
        super().__init__()
        self.menuItems = [
            {"title": "Play", "action": lambda: print("Mock")},
            {"title": "Quit", "action": lambda: self.exitMenu()},
        ]
        self.font = pygame.font.Font(None, 16)
        self.textColor = (255, 255, 255)
        self.currentItemIndex = 0

    def exitMenu(self):
        self.notifyQuitRequested()

    def update(self):
        pass

    def render(self, window):
        window.fill((0, 0, 0))
        selectedColor = (34, 139, 34)
        gap = 40

        self.renderTitle(window)

        for index, menuItem in enumerate(self.menuItems):
            textColor = (
                selectedColor if self.currentItemIndex == index else self.textColor
            )

            # Render the text
            textSurface = self.font.render(menuItem["title"], True, textColor)

            # Get the rectangle containing the text surface
            textRect = textSurface.get_rect()

            # Center the text on the screen
            textRect.center = (640 // 2, 480 // 2 + gap * index)

            # Blit the text surface onto the main surface
            window.blit(textSurface, textRect)

        pygame.display.update()

    def renderTitle(self, window):
        textSurface = self.font.render("Bomberman", True, self.textColor)

        # Get the rectangle containing the text surface
        textRect = textSurface.get_rect()

        # Center the text on the screen
        textRect.center = (640 // 2, 480 // 2 - 2 * 40)

        # Blit the text surface onto the main surface
        window.blit(textSurface, textRect)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitMenu()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exitMenu()
                    break
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    self.menuItems[self.currentItemIndex]["action"]()
                elif event.key == pygame.K_DOWN:
                    self.currentItemIndex = (self.currentItemIndex + 1) % len(
                        self.menuItems
                    )
                elif event.key == pygame.K_UP:
                    self.currentItemIndex = (self.currentItemIndex - 1) % len(
                        self.menuItems
                    )
