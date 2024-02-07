import pygame
from pygame import Surface

DAMAGE = 25


class Laser:
    def __init__(self, x: float, y: float, width: float, height: float, velocity: tuple[float, float],
                 surface: Surface):
        self.height = height * 0.5
        self.width = width * 0.2
        self.x = x + width * 0.5 - self.width * 0.5
        self.y = y
        self.picture = surface
        self.surface = pygame.mask.from_surface(surface)

        self.velocity = velocity
        self.damage = DAMAGE
        self.collided = False

    def update_laser_coordinates(self):
        self.x += self.velocity[0]
        self.y -= self.velocity[1]

    def above_screen(self) -> bool:
        return (self.y + self.height) < 0

    def below_screen(self, window_height: int) -> bool:
        return self.y > window_height

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int,
                                     new_ship_width: int, new_ship_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = new_ship_width * 0.5
        self.height = new_ship_height * 0.2
