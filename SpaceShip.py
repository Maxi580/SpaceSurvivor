import pygame
from pygame import Surface
from math import sqrt
from Laser import Laser
from ObjectInterface import Entity


class SpaceShip(Entity):
    def __init__(self, width: int, height: int, surface: Surface, hp: int, velocity: int, shot_velocity: int):
        self.width = width * 0.1
        self.height = height * 0.1
        self.x = width * 0.5 - self.width * 0.5
        self.y = height * 0.8

        self.picture = pygame.transform.scale(surface, (self.width, self.height))
        self.surface = pygame.mask.from_surface(self.picture)

        self.x_velocity = sqrt((velocity ** 2) / 2)
        self.y_velocity = self.x_velocity

        self.shot_velocity = shot_velocity
        self.hp = hp
        self.movement_directions = {"left": False, "right": False, "up": False, "down": False}
        self.immune = False
        self.immune_counter = 0

    def update_coordinates(self, screen_width: int, screen_height: int):
        movement_count = sum(self.movement_directions.values())
        if movement_count == 2:
            x_velocity = self.x_velocity
            y_velocity = self.y_velocity
        else:
            x_velocity = sqrt(self.x_velocity**2 + self.y_velocity**2)
            y_velocity = x_velocity

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

    def shoot(self, surface) -> Laser:
        return Laser(self.x, self.y, self.width, self.height, (0, self.shot_velocity), surface)

    def set_immune(self):
        self.immune = True

    def is_immune(self) -> bool:
        return self.immune

    def get_immune_counter(self) -> int:
        return self.immune_counter

    def reset_immune(self):
        if self.immune_counter > 100:
            self.immune = False
            self.immune_counter = 0

    def increase_immune_counter(self):
        self.immune_counter += 1

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def get_hp(self) -> int:
        return self.hp

    def reduce_hp(self, amount):
        self.hp -= amount

    def update_size(self, new_window_width: int, new_window_height: int,
                    old_window_width: int, old_window_height: int):
        self.x *= (new_window_width / old_window_width)
        self.y *= (new_window_height / old_window_height)

        self.x_velocity *= (new_window_width / old_window_width)
        self.y_velocity *= (new_window_height / old_window_height)

        self.width *= (new_window_width / old_window_width)
        self.height *= (new_window_height / old_window_height)
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))
        self.surface = pygame.mask.from_surface(self.picture)


