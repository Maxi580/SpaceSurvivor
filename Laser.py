import pygame
from pygame import Surface


class Laser:
    def __init__(self, x: float, y: float, width: float, height: float, surface: Surface):
        self.height = height * 0.5
        self.width = width * 0.2
        self.x = x + width * 0.5 - self.width * 0.5
        self.y = y
        self.surface = pygame.mask.from_surface(surface)

        self.velocity = 14
        self.damage = 25
        self.collided = False

    def update_laser_coordinates(self):
        self.y -= self.velocity

    def above_screen(self) -> bool:
        return (self.y + self.height) < 0

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int,
                                     new_ship_width: int, new_ship_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = new_ship_width * 0.5
        self.height = new_ship_height * 0.2

