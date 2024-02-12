import math
from math import sqrt

import pygame
from pygame import Surface
from ObjectInterface import Entity

DAMAGE = 25


class Laser(Entity):
    def __init__(self, x: float, y: float, width: float, height: float, velocity: tuple[float, float],
                 surface: Surface):
        self.height = height * 0.5
        self.width = width * 0.2
        self.x = x + width * 0.5 - self.width * 0.5
        self.y = y
        self.x_velocity = velocity[0]
        self.y_velocity = velocity[1]

        scaled_surface = pygame.transform.scale(surface, (self.width, self.height))
        angle_radians = math.atan2(self.x_velocity, self.y_velocity)
        angle_degrees = math.degrees(angle_radians)
        self.picture = pygame.transform.rotate(scaled_surface, -angle_degrees)
        self.surface = pygame.mask.from_surface(self.picture)

        self.damage = DAMAGE
        self.collided = False

    def update_coordinates(self):
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def above_screen(self) -> bool:
        return (self.y + self.height) < 0

    def below_screen(self, window_height: int) -> bool:
        return self.y > window_height

    def adjust_velocity_to_window_resize(self, old_window_width: int, old_window_height: int,
                                         new_window_width: int, new_window_height: int):
        self.x_velocity *= (new_window_width / old_window_width)
        self.y_velocity *= (new_window_height / old_window_height)

    def get_collided(self):
        return self.collided
