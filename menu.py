from pygame.math import Vector2
import pygame


class Menu:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Bomberman")
        self.window = pygame.display.set_mode((640, 480))

        self.running = True
        self.clock = pygame.time.Clock()
        self.menuItems = [
            {"title": "Play", "action": lambda: print("Mock")},
            {"title": "Quit", "action": lambda: self.exitMenu()},
        ]
        self.currentItemIndex = 0
        self.font = pygame.font.Font(None, 16)
        self.textColor = (255, 255, 255)

    def run(self):
        while self.running:
            self.processInput()
            self.render()
            self.clock.tick(60)

    def exitMenu(self):
        self.running = False

    def render(self):
        self.window.fill((0, 0, 0))
        selectedColor = (34, 139, 34)
        gap = 40

        self.renderTitle()

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
            self.window.blit(textSurface, textRect)

        pygame.display.update()

    def renderTitle(self):
        textSurface = self.font.render("Bomberman", True, self.textColor)

        # Get the rectangle containing the text surface
        textRect = textSurface.get_rect()

        # Center the text on the screen
        textRect.center = (640 // 2, 480 // 2 - 2 * 40)

        # Blit the text surface onto the main surface
        self.window.blit(textSurface, textRect)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitMenu()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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


menu = Menu()
menu.run()
