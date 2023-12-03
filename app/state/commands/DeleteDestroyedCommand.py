from pygame.math import Vector2
from .Command import Command


class DeleteDestroyedCommand(Command):
    def __init__(self, bullets) -> None:
        super().__init__()
        self.bullets = bullets

    def run(self):
        for bullet in self.bullets:
            if bullet.status == "destroyed":
                self.bullets.remove(bullet)
