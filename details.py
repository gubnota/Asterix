import random
from typing import Any

import pygame

import settings


romans = pygame.sprite.Group()


class Roman(pygame.sprite.Sprite):
    """Класс Римлянина."""

    def __init__(self):
        self.WIGHT_OF_SCREEN = pygame.display.get_surface().get_width()
        self.HEIGHT_OF_SCREEN = pygame.display.get_surface().get_height()

        self.PLACES_OF_BIRTH = (
            random.randint(settings.ROMANS_INDENT, self.WIGHT_OF_SCREEN),
            random.randint(settings.ROMANS_INDENT, self.HEIGHT_OF_SCREEN)
        )

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(settings.PATH_TO_ROMANS),
            settings.ROMANS_SIZE
        ).convert_alpha()
        self.image.set_colorkey(settings.BLACK_COLOR)
        self.rect = self.image.get_rect(
            center=self.PLACES_OF_BIRTH
        )
        self.vectors = [
            self.go_up,
            self.go_down,
            self.go_right,
            self.go_left,
        ]
        self.go_vectors = []

    def go_left(self):
        self.rect.x -= settings.ROMANS_SPEED
        if self.rect.x <= 0:
            self.rect.x = 0

    def go_right(self):
        self.rect.x += settings.ROMANS_SPEED
        if self.rect.x >= self.WIGHT_OF_SCREEN - self.rect.width:
            self.rect.x = self.WIGHT_OF_SCREEN - self.rect.width

    def go_up(self):
        self.rect.y -= settings.ROMANS_SPEED
        if self.rect.y <= 0:
            self.rect.y = 0

    def go_down(self):
        self.rect.y += settings.ROMANS_SPEED
        if self.rect.y >= self.HEIGHT_OF_SCREEN - self.rect.height:
            self.rect.y = self.HEIGHT_OF_SCREEN - self.rect.height

    def add_go_vectors(self, vector):
        self.go_vectors = [vector] * settings.ROMANS_SMOOTHNESS

    def go(self):
        if not self.go_vectors:
            vector = random.choice(self.vectors)
            self.add_go_vectors(vector)
        self.go_vectors.pop()()

    def update(self, asterix_rect) -> None:
        self.go()
        if self.rect.colliderect(asterix_rect):
            settings.START_SCORE += settings.SCORE_INCREASE
            self.kill()


class MagicFlask(pygame.sprite.Sprite):
    """Класс фляжки с волшебным напитком."""
    SUPER_POWER_TIME_OUT = settings.ASTERIX_SUPER_POWER_TIME_OUT

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(settings.PATH_TO_FLASK)
        self.rect = self.image.get_rect(center=settings.FLASK_POSITION)

    def update(self, asterix_rect) -> None:
        if self.rect.colliderect(asterix_rect):
            settings.ASTERIX_HAS_SUPER_POWER = True
            settings.ASTERIX_SUPER_POWER_TIME_OUT = self.SUPER_POWER_TIME_OUT
            self.kill()
