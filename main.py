import pygame
from pygame.math import Vector2
from app.state import GameState
from app.ui import UserInterface
from app.state.commands import MoveCommand


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Bomberman")
        # pygame.display.set_icon(pygame.image.load("icon.png"))
        self.clock = pygame.time.Clock()
        self.gameState = GameState()
        self.ui = UserInterface(self.gameState)

    def run(self):
        while self.running:
            self.ui.processInput()
            self.ui.update()
            self.ui.render()
            self.clock.tick(60)


game = Game()
game.run()
