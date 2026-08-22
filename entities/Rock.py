import pygame
from pygame import Surface
from ObjectInterface import Entity

DAMAGE = 25


class Rock(Entity):
    def __init__(self, x: int, screen_width: int, screen_height: int, size: int, surface: Surface, velocity: float,
                 hp: int):
        self.width = size * (screen_width / 8)
        self.height = size * (screen_height / 8)
        self.x = x - self.width * 0.5
        self.y = -self.height

        self.picture = pygame.transform.scale(surface, (self.width, self.height))
        self.surface = pygame.mask.from_surface(self.picture)

        self.size = size
        self.hp = hp * size
        self.velocity = velocity
        self.damage = DAMAGE

    def update_coordinates(self):
        self.y += self.velocity

    def below_screen(self, height) -> bool:
        return self.y > height

    def update_middle_surface(self, surface):
        if self.hp <= 100:
            self.picture = pygame.transform.scale(surface, (self.width, self.height))
            self.surface = pygame.mask.from_surface(self.picture)

    def update_big_surface(self, surface_100hp, surface_200hp):
        if 100 < self.hp <= 200:
            self.picture = pygame.transform.scale(surface_200hp, (self.width, self.height))
            self.surface = pygame.mask.from_surface(self.picture)
        elif self.hp <= 100:
            self.picture = pygame.transform.scale(surface_100hp, (self.width, self.height))
            self.surface = pygame.mask.from_surface(self.picture)

    def update_size(self, new_window_width: int, new_window_height: int,
                    old_window_width: int, old_window_height: int):
        self.x *= (new_window_width / old_window_width)
        self.y *= (new_window_height / old_window_height)

        self.velocity *= (new_window_height / old_window_height)

        self.width *= (new_window_width / old_window_width)
        self.height *= (new_window_height / old_window_height)
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))
        self.surface = pygame.mask.from_surface(self.picture)
