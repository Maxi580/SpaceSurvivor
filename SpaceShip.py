import pygame
from pygame import Surface
from math import sqrt
from Laser import Laser


class SpaceShip:
    def __init__(self, width: int, height: int, surface: Surface):
        self.width = width * 0.1
        self.height = height * 0.1
        self.x = width * 0.5 - self.width * 0.5
        self.y = height * 0.8
        self.picture = surface
        self.surface = pygame.mask.from_surface(surface)

        self.x_velocity = 7
        self.y_velocity = 7
        self.shot_velocity = 14
        self.hp = 100
        self.movement_directions = {"left": False, "right": False, "up": False, "down": False}
        self.immune = False
        self.immune_counter = 0

    def update_space_ship_coordinates(self, screen_width: int, screen_height: int):
        movement_count = sum(self.movement_directions.values())
        if movement_count == 2:
            y_velocity = sqrt((self.y_velocity ** 2) / 2)
            x_velocity = sqrt((self.x_velocity ** 2) / 2)
        else:
            y_velocity = self.y_velocity
            x_velocity = self.x_velocity

        if self.movement_directions.get("left"):
            new_x_coordinate = self.x - x_velocity
            if new_x_coordinate > 0:
                self.x = new_x_coordinate
            else:
                self.x = 0
        if self.movement_directions.get("right"):
            new_x_coordinate = self.x + x_velocity
            x_maximum = (screen_width - self.width)
            if new_x_coordinate < x_maximum:
                self.x = new_x_coordinate
            else:
                self.x = x_maximum
        if self.movement_directions.get("up"):
            new_y_coordinate = self.y - y_velocity
            if new_y_coordinate > 0:
                self.y = new_y_coordinate
            else:
                self.y = 0
        if self.movement_directions.get("down"):
            new_y_coordinate = self.y + y_velocity
            y_minimum = (screen_height - self.height)
            if new_y_coordinate < y_minimum:
                self.y = new_y_coordinate
            else:
                self.y = y_minimum

    def start_movement(self, direction: str):
        if direction == "LEFT":
            self.movement_directions["left"] = True
        elif direction == "RIGHT":
            self.movement_directions["right"] = True
        elif direction == "UP":
            self.movement_directions["up"] = True
        elif direction == "DOWN":
            self.movement_directions["down"] = True

    def stop_movement(self, direction: str):
        if direction == "LEFT":
            self.movement_directions["left"] = False
        elif direction == "RIGHT":
            self.movement_directions["right"] = False
        elif direction == "UP":
            self.movement_directions["up"] = False
        elif direction == "DOWN":
            self.movement_directions["down"] = False

    def take_hit(self, damage):
        self.hp -= damage

    def shoot(self, surface):
        return Laser(self.x, self.y, self.width, self.height, (0, self.shot_velocity), surface)

    def set_immune(self):
        self.immune = True

    def get_immune(self):
        return self.immune

    def get_immune_counter(self):
        return self.immune_counter

    def reset_immune(self):
        if self.immune_counter > 100:
            self.immune = False
            self.immune_counter = 0

    def increase_immune_counter(self):
        self.immune_counter += 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_hp(self):
        return self.hp

    def reduce_hp(self, amount):
        self.hp -= amount

    def adjust_velocity_to_window_resize(self, old_window_width: int, old_window_height: int,
                                         new_window_width: int, new_window_height: int):
        self.y_velocity *= (new_window_height / old_window_height)
        self.x_velocity *= (new_window_width / old_window_width)
        self.shot_velocity *= (new_window_height / old_window_height)


