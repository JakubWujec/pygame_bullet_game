import pygame

from .GameMode import GameMode


class MenuGameMode(GameMode):
    def __init__(self) -> None:
        super().__init__()
        self.menuItems = [
            {
                "title": "Level 1",
                "action": lambda: self.notifyLoadLevelRequested(
                    "app/assets/levels/level_1.tmx"
                ),
            },
            {
                "title": "Level 2",
                "action": lambda: self.notifyLoadLevelRequested(
                    "app/assets/levels/level_2.tmx"
                ),
            },
            {"title": "Quit", "action": self.notifyQuitRequested},
        ]
        self.font = pygame.font.Font(None, 48)
        self.textColor = (255, 255, 255)
        self.selectedColor = (34, 139, 34)
        self.currentItemIndex = 0

    def update(self):
        pass

    def render(self, window):
        self.renderTitle(window)
        self.renderMenuItems(window)

    def renderMenuItems(self, window):
        gap = 60
        windowWidth, windowHeight = window.get_size()
        for index, menuItem in enumerate(self.menuItems):
            textColor = (
                self.selectedColor if self.currentItemIndex == index else self.textColor
            )

            # Render the text
            textSurface = self.font.render(menuItem["title"], True, textColor)

            # Get the rectangle containing the text surface
            textRect = textSurface.get_rect()

            # Center the text on the screen
            textRect.center = (windowWidth // 2, windowHeight // 2 + gap * index)

            # Blit the text surface onto the main surface
            window.blit(textSurface, textRect)

    def renderTitle(self, window):
        windowWidth, windowHeight = window.get_size()
        textSurface = self.font.render("Bullet Game", True, self.textColor)

        # Get the rectangle containing the text surface
        textRect = textSurface.get_rect()

        # Center the text on the screen
        textRect.center = (windowWidth // 2, 150)

        # Blit the text surface onto the main surface
        window.blit(textSurface, textRect)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowGameRequested()
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
