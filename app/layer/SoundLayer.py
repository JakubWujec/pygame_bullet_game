import pygame
from pygame.math import Vector2

from .Layer import Layer


class SoundLayer(Layer):
    def __init__(self):
        self.explosion_sound = pygame.mixer.Sound("./app/assets/sound/explosion.mp3")
        self.match_struck_sound = pygame.mixer.Sound(
            "./app/assets/sound/match_struck.mp3"
        )

    def bulletFired(self):
        pygame.mixer.Sound.play(self.match_struck_sound)
        pygame.mixer.music.stop()

    def bulletExploded(self):
        pygame.mixer.Sound.play(self.explosion_sound)
        pygame.mixer.music.stop()

    def render(self, surface):
        pass
