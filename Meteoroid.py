import pygame
from pygame import Surface

DAMAGE = 25
VELOCITY = 7


class Meteoroid:
    def __init__(self, x: int, width: int, screen_height: int, surface: Surface):
        self.width = width
        self.height = screen_height / 2
        self.x = x
        self.y = -self.height
        self.surface = pygame.mask.from_surface(surface)
        self.picture = surface

        self.hp = 100
        self.velocity = VELOCITY
        self.damage = DAMAGE

    def below_screen(self, window_height: int) -> bool:
        return self.y > window_height

    def update_coordinates(self):
        self.y += self.velocity

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = self.size * (new_window_width / 8)
        self.height = self.size * (new_window_height / 8)

