import pygame
from pygame.math import Vector2
from app.state import GameState
from app.ui import UserInterface


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Discover Python & Patterns")
        # pygame.display.set_icon(pygame.image.load("icon.png"))
        self.clock = pygame.time.Clock()
        self.gameState = GameState()
        self.moveTankCommand = Vector2(0, 0)
        self.ui = UserInterface(self.gameState)

        self.running = True

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                if event.key == pygame.K_RIGHT:
                    self.moveTankCommand = Vector2(1, 0)
                elif event.key == pygame.K_LEFT:
                    self.moveTankCommand = Vector2(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.moveTankCommand = Vector2(0, 1)
                elif event.key == pygame.K_UP:
                    self.moveTankCommand = Vector2(0, -1)

    def update(self):
        self.gameState.update(self.moveTankCommand)
        self.moveTankCommand = Vector2(0, 0)

    def render(self):
        self.ui.render()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()


game = Game()
game.run()
