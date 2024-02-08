from math import sqrt

import pygame
from pygame import Surface

SHIP_VELOCITY = 3.5
VELOCITY = 7
MAX_HP = 250


class Alien:
    def __init__(self, x: float, screen_width: float, screen_height: float, surface: Surface):
        self.width = screen_width * 0.1
        self.height = screen_height * 0.1
        self.x = self.assign_x_value(x, screen_width)
        self.y = -self.height
        self.picture = surface
        self.surface = pygame.mask.from_surface(surface)

        self.max_hp = MAX_HP
        self.hp = self.max_hp
        self.ship_velocity = SHIP_VELOCITY
        self.shot_velocity = VELOCITY
        self.velocity = 7

    def calculate_shot_velocity(self, target_x, target_y) -> tuple[float, float]:
        """First: Calculate x/ y difference to target
           Then: scale it so that x**2 + y**2 == 7**2"""
        x_difference = target_x - self.x
        y_difference = target_y - self.y

        if x_difference == 0:
            if y_difference < 0:
                return 0, self.shot_velocity
            else:
                return 0, -self.shot_velocity
        if y_difference == 0:
            if x_difference < 0:
                return self.shot_velocity, 0
            else:
                return -self.shot_velocity, 0

        x_size_relative_to_y = (x_difference / y_difference)

        right_side_of_pythagoras = (self.shot_velocity ** 2) / (x_size_relative_to_y ** 2 + 1)
        if y_difference > 0:
            y_velocity = -sqrt(right_side_of_pythagoras)
        else:
            y_velocity = sqrt(right_side_of_pythagoras)

        if x_difference > 0:
            x_velocity = sqrt((self.shot_velocity ** 2) - y_velocity ** 2)
        else:
            x_velocity = -sqrt((self.shot_velocity ** 2) - y_velocity ** 2)

        return x_velocity, y_velocity

    def move_to_position(self, position_y):
        if self.y < (position_y - self.velocity):
            self.y += self.ship_velocity
        elif (position_y - self.velocity) < self.y < position_y or self.y > position_y:
            self.y = position_y

    def assign_x_value(self, x: float, screen_width: float) -> float:
        if x == 0:
            return 0
        elif x < screen_width:
            return x - (self.width * 0.5)
        else:
            return x - self.width

    def adjust_velocity_to_window_resize(self, old_window_width: int, old_window_height: int,
                                         new_window_width: int, new_window_height: int):
        self.velocity *= (new_window_height / old_window_height)

    def get_max_hp(self):
        return self.max_hp

    def get_hp(self):
        return self.hp

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


