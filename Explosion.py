import pygame
from pygame import Surface

from Rock import Rock
from SpaceShip import SpaceShip


class Explosion:
    def __init__(self, x: int, y: int, width: int, height: int, surface: Surface,
                 size_factor: float, colliding_rock: Rock = None, colliding_spaceship: SpaceShip = None):
        self.stage = 0
        self.age = 0
        self.age_factor = 3

        self.width = width * size_factor
        self.height = height * size_factor
        self.picture = pygame.transform.scale(surface, (self.width, self.height))

        self.x = x + 0.5 * width - self.width * 0.5
        self.y = y + 0.5 * height - self.height * 0.5

        self.colliding_rock = colliding_rock
        self.colliding_spaceship = colliding_spaceship

    def adjust_stage_to_age(self):
        """Every 3 (self.age_factor) age increases the stage gets increased"""
        if self.age > (self.stage * self.age_factor):
            self.stage += 1
            return True
        else:
            return False

    def adjust_picture_to_stage(self, picture: Surface):
        self.picture = pygame.transform.scale(picture, (self.width, self.height))

    def adjust_y_to_movement_of_object(self):
        self.y += self.colliding_rock.velocity

    def increase_age(self, amount):
        self.age += amount

    def get_stage(self):
        return self.stage

    def get_colliding_rock(self):
        return self.colliding_rock

    def get_colliding_spaceship(self):
        return self.colliding_spaceship

    def adjust_coordinates_to_spaceship(self):
        self.x = self.colliding_spaceship.get_x() + 0.5 * self.colliding_spaceship.get_width() - self.width * 0.5
        self.y = self.colliding_spaceship.get_y() + 0.5 * self.colliding_spaceship.get_height() - self.width * 0.5






