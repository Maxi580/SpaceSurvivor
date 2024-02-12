import math
import random
from math import sqrt

import pygame

from ObjectInterface import Entity


class Rocket(Entity):
    def __init__(self, velocity, width, height, x, y, surface):
        self.height = height * 1.2
        self.width = width
        self.x = x + width * 0.5 - self.width * 0.5
        self.y = y
        self.damage = 25
        self.hp = 1

        self.picture = pygame.transform.scale(surface, (self.width, self.height))
        self.non_rotated_picture = self.picture
        self.surface = pygame.mask.from_surface(self.picture)

        self.x_velocity = random.uniform(-velocity, velocity)
        self.y_velocity = sqrt(velocity**2 - self.x_velocity**2)
        self.calculate_direction()

    def update_coordinates(self, width, height):
        #  Left Border
        if (self.x + self.x_velocity) <= 0:
            self.x = 0
        #  Right Border
        elif (self.x + self.width + self.x_velocity) >= width:
            self.x = width - self.width
        #  Top Border
        elif (self.y + self.y_velocity) <= 0:
            self.y = 0
        #  Bottom Border
        elif (self.y + self.height + self.y_velocity) >= height:
            self.y = height - self.height
        else:
            self.x += self.x_velocity
            self.y += self.y_velocity

    def return_at_border(self, width, height):
        if self.x == 0 or (self.x + self.width) == width:
            self.x_velocity *= -1
            self.calculate_direction()
        if self.y == 0 or (self.y + self.height) == height:
            self.y_velocity *= -1
            self.calculate_direction()

    def calculate_direction(self):
        angle_radians = math.atan2(self.x_velocity, self.y_velocity)
        angle_degrees = math.degrees(angle_radians)
        scaled_non_rotated_picture = pygame.transform.scale(self.non_rotated_picture, (self.width, self.height))
        self.picture = pygame.transform.rotate(scaled_non_rotated_picture, angle_degrees)
        self.surface = pygame.mask.from_surface(self.picture)

    def adjust_velocity_to_window_resize(self, old_window_width: int, old_window_height: int,
                                         new_window_width: int, new_window_height: int):

        self.x_velocity *= (new_window_width / old_window_width)
        self.y_velocity *= (new_window_height / old_window_height)



