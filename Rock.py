import pygame
from pygame import Surface

DAMAGE = 25


#  Observer Pattern


class Rock:
    def __init__(self, x: int, screen_width: int, screen_height: int, size: int, surface: Surface):
        self.width = size * (screen_width / 8)
        self.height = size * (screen_height / 8)
        self.x = x - self.width * 0.5
        self.y = -self.height
        self.surface = pygame.mask.from_surface(surface)
        self.picture = surface

        self.size = size
        self.hp = 100 * size
        self.velocity = self.get_velocity()
        self.damage = DAMAGE

    def update_rock_coordinates(self):
        self.y += self.velocity

    def below_screen(self, height) -> bool:
        return self.y > height

    def get_velocity(self) -> int:
        if self.size == 1:
            return 6
        elif self.size == 2:
            return 5
        else:
            return 4

    def update_middle_surface(self, surface):
        if self.hp <= 100:
            self.surface = pygame.mask.from_surface(surface)
            self.picture = surface

    def update_big_surface(self, surface_100hp, surface_200hp):
        if 100 < self.hp <= 200:
            self.surface = pygame.mask.from_surface(surface_200hp)
            self.picture = surface_200hp
        elif self.hp <= 100:
            self.surface = pygame.mask.from_surface(surface_100hp)
            self.picture = surface_100hp

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = self.size * (new_window_width / 8)
        self.height = self.size * (new_window_height / 8)
