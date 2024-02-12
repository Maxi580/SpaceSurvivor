import pygame
from pygame import Surface

DAMAGE = 25


class Rock:
    def __init__(self, x: int, screen_width: int, screen_height: int, size: int, surface: Surface, velocity: float):
        self.width = size * (screen_width / 8)
        self.height = size * (screen_height / 8)
        self.x = x - self.width * 0.5
        self.y = -self.height
        self.surface = pygame.mask.from_surface(surface)
        self.picture = surface

        self.size = size
        self.hp = 100 * size
        self.velocity = velocity
        print(self.velocity)
        self.damage = DAMAGE

    def update_rock_coordinates(self):
        self.y += self.velocity

    def below_screen(self, height) -> bool:
        return self.y > height

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

    def adjust_velocity_to_window_resize(self, old_window_width: int, old_window_height: int,
                                         new_window_width: int, new_window_height: int):
        self.velocity *= (new_window_height / old_window_height)
        print(self.velocity)
