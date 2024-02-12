import math
import random
from math import sqrt

import pygame

from ObjectInterface import Entity


def find_leftmost_pixel(image):
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            alpha = image.get_at((x, y))[3]
            if alpha != 0:
                return x
    return None


def find_rightmost_pixel(image):
    for x in range(image.get_width() - 1, -1, -1):
        for y in range(image.get_height()):
            alpha = image.get_at((x, y))[3]
            if alpha != 0:
                return x
    return None


def find_highest_pixel(image):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            alpha = image.get_at((x, y))[3]
            if alpha != 0:
                return y
    return None


def find_lowest_pixel(image):
    for y in range(image.get_height() - 1, -1, -1):
        for x in range(image.get_width()):
            alpha = image.get_at((x, y))[3]
            if alpha != 0:
                return y
    return None


class Rocket(Entity):
    def __init__(self, velocity, width, height, x, y, surface):
        self.height = height * 0.3
        self.width = width * 0.1
        self.x = x + width * 0.5 - self.width * 0.5
        self.y = y + height
        self.damage = 25
        self.hp = 1

        self.picture = pygame.transform.scale(surface, (self.width, self.height))
        self.non_rotated_picture = self.picture
        self.surface = pygame.mask.from_surface(self.picture)

        self.x_velocity = random.uniform(-velocity, velocity)
        self.y_velocity = sqrt(velocity**2 - self.x_velocity**2)
        self.calculate_direction()

    def update_coordinates(self, width, height):
        left_x = find_leftmost_pixel(self.picture) + self.x
        right_x = find_rightmost_pixel(self.picture) + self.x
        top_y = find_highest_pixel(self.picture) + self.y
        bottom_y = find_lowest_pixel(self.picture) + self.y

        #  Left Border
        if (left_x + self.x_velocity) <= 0:
            self.x_velocity *= -1
            self.calculate_direction()
        #  Right Border
        if (right_x + self.x_velocity) >= width:
            self.x_velocity *= -1
            self.calculate_direction()
        if (top_y + self.y_velocity) <= 0:
            self.y_velocity *= -1
            self.calculate_direction()
        #  Bottom Border
        if (bottom_y + self.y_velocity) >= height:
            self.y_velocity *= -1
            self.calculate_direction()
        self.x += self.x_velocity
        self.y += self.y_velocity

    def return_at_border(self, width, height):
        left_x = find_leftmost_pixel(self.picture) + self.x
        right_x = find_rightmost_pixel(self.picture) + self.x
        top_y = find_highest_pixel(self.picture) + self.y
        bottom_y = find_lowest_pixel(self.picture) + self.y

        if left_x == 0 or right_x == width:
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



