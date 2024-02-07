import pygame
from pygame import Surface


class Explosion:
    def __init__(self, ship_x: int, ship_y: int, ship_width: int, ship_height: int, surface: Surface):
        self.stage = 0
        self.age = 0
        self.age_factor = 3
        self.picture = surface

        self.width = ship_width
        self.height = ship_height
        self.x = ship_x + 0.5 * ship_width - self.width * 0.5
        self.y = ship_y + 0.5 * ship_height - self.height * 0.5

    def adjust_stage_to_age(self):
        """Every 3 (self.age_factor) self.age increases the stage gets increased"""
        if self.age > (self.stage * self.age_factor):
            self.stage += 1
            return True
        else:
            return False

    def adjust_picture_to_stage(self, picture: Surface):
        self.picture = picture




