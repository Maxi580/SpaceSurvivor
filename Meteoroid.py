import pygame
from pygame import Surface
from ObjectInterface import Entity

DAMAGE = 25


class Meteoroid(Entity):
    def __init__(self, x: float, width: float, screen_height: int, surface: Surface, velocity: int):
        self.width = width
        self.height = screen_height / 2
        self.x = x
        self.y = -self.height

        self.picture = pygame.transform.scale(surface, (self.width, self.height))
        self.surface = pygame.mask.from_surface(self.picture)

        self.hp = 1
        self.velocity = velocity
        self.damage = DAMAGE

    def below_screen(self, window_height: int) -> bool:
        return self.y > window_height

    def update_coordinates(self):
        self.y += self.velocity

    def adjust_velocity_to_window_resize(self, old_window_width: int, old_window_height: int,
                                         new_window_width: int, new_window_height: int):
        self.velocity *= (new_window_height / old_window_height)
