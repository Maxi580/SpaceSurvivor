import random
from enum import Enum, auto

import pygame
import pygame.freetype
from pygame import Rect
from pygame.rect import RectType
from win32api import GetSystemMetrics

from Laser import Laser
from Rock import Rock
from SpaceShip import SpaceShip


class GamePhase(Enum):
    ROCKS = auto()
    ALIENS = auto()


def blend_color(color1, color2, blend_factor):
    r = color1[0] + (color2[0] - color1[0]) * blend_factor
    g = color1[1] + (color2[1] - color1[1]) * blend_factor
    b = color1[2] + (color2[2] - color1[2]) * blend_factor
    return int(r), int(g), int(b)


def apply_vertical_gradient(surface, start_color, end_color):
    height = surface.get_height()
    for y in range(height):
        blend = y / height
        color = blend_color(start_color, end_color, blend)
        for x in range(surface.get_width()):
            pixel = surface.get_at((x, y))
            surface.set_at((x, y), color + (pixel[3],))


class App:
    def __init__(self):
        pygame.init()

        self.images = load_images()
        self.start_color = (0, 255, 0)
        self.end_color = (0, 128, 0)

        self.screen_width = GetSystemMetrics(0) * 0.25
        self.screen_height = GetSystemMetrics(1) * 0.6
        self.screen = self.initialize_screen()

        self.spaceship: SpaceShip = SpaceShip(self.screen_width, self.screen_height, self.images['spaceship'])
        self.key_to_attr = {pygame.K_a: 'LEFT',
                            pygame.K_w: 'UP',
                            pygame.K_s: 'DOWN',
                            pygame.K_d: 'RIGHT'}

        self.lasers: list[Laser] = []

        self.rocks: list[Rock] = []
        self.rock_spawn_start_probability = 0.0025
        self.rock_spawn_increment_probability = 0.0025
        self.rock_spawn_probability = self.rock_spawn_start_probability

        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.ROCKS
        self.end_of_first_phase = 250
        self.score = 0
        self.running = True

    def initialize_screen(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)

        background = self.images["background"]
        scaled_background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        screen.blit(scaled_background, (0, 0))

        pygame.display.update()

        return screen

    def reset_screen(self):
        background = self.images["background"]
        scaled_background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        self.screen.blit(scaled_background, (0, 0))

    def update_screen_size(self, width, height):
        self.spaceship.adjust_size_to_window_resize(self.screen_width, self.screen_height, width, height)
        for laser in self.lasers:
            laser.adjust_size_to_window_resize(self.screen_width, self.screen_height, width, height,
                                               self.spaceship.width, self.spaceship.height)

        self.screen_width = width
        self.screen_height = height

    def draw_game_info(self, pos, text: str):
        """Lädt einen Text, wendet darauf einen Farbverlauf an und zeichnet ihn."""
        font = pygame.font.SysFont('Raleway Bold', int(0.1 * self.screen_width))
        surface = font.render(text, True, (0, 0, 0))

        apply_vertical_gradient(surface, self.start_color, self.end_color)

        if pos[0] == 0:
            x = pos[0] + self.screen_width * 0.0025
        else:
            x = self.screen_width * 0.9975 - surface.get_width()
        self.screen.blit(surface, (x, pos[1]))

    def create_rock(self, x, size):
        surfaces = [self.images["smallRock100HP"], self.images["middleRock200HP"], self.images["bigRock300HP"]]
        return Rock(x, self.screen_width, self.screen_height, size, surfaces[size - 1])

    def spawn_rock(self):
        if random.random() < self.rock_spawn_probability:
            random_size_number = random.random()
            if random_size_number <= 0.35:
                new_rock = self.create_rock(random.randint(0, self.screen_width), 1)
            elif random_size_number <= 0.75:
                new_rock = self.create_rock(random.randint(0, self.screen_width), 2)
            else:
                new_rock = self.create_rock(random.randint(0, self.screen_width), 3)
            self.rocks.append(new_rock)
            self.rock_spawn_probability = self.rock_spawn_start_probability
        else:
            self.rock_spawn_probability += self.rock_spawn_increment_probability

    def draw_rocks(self) -> list[Rect | RectType]:
        rock_drawings: list[Rect | RectType] = []
        for rock in self.rocks:
            scaled_rock_picture = pygame.transform.scale(rock.picture, (rock.width, rock.height))
            rock.surface = pygame.mask.from_surface(scaled_rock_picture)
            rock_drawing = self.screen.blit(scaled_rock_picture, (rock.x, rock.y))
            rock_drawings.append(rock_drawing)
        return rock_drawings

    def eliminate_rocks(self):
        i = 0
        while i < len(self.rocks):
            if self.rocks[i].hp <= 0:
                self.rocks.pop(i)
            else:
                i += 1

    def draw_space_ship(self) -> Rect | RectType:
        spaceship_picture = self.images["spaceship"]
        scaled_spaceship_picture = pygame.transform.scale(spaceship_picture,
                                                          (self.spaceship.width, self.spaceship.height))
        self.spaceship.surface = pygame.mask.from_surface(scaled_spaceship_picture)
        return self.screen.blit(scaled_spaceship_picture, (self.spaceship.x, self.spaceship.y))

    def spaceship_rock_collisions(self):
        for rock in self.rocks:
            offset_x = self.spaceship.x - rock.x
            offset_y = self.spaceship.y - rock.y
            if rock.surface.overlap(self.spaceship.surface, (offset_x, offset_y)):
                self.spaceship.hp -= rock.damage
                rock.hp = 0

    def eliminate_player(self):
        if self.spaceship.hp <= 0:
            print("Lost")
            self.running = False
            pygame.quit()

    def draw_lasers(self) -> list[Rect | RectType]:
        laser_picture = self.images["laser"]
        laser_drawings: list[Rect | RectType] = []
        for laser in self.lasers:
            scaled_spaceship_picture = pygame.transform.scale(laser_picture,
                                                              (laser.width, laser.height))
            laser_drawing = self.screen.blit(scaled_spaceship_picture, (laser.x, laser.y))
            laser_drawings.append(laser_drawing)
        return laser_drawings

    def laser_rock_collisions(self):
        for laser in self.lasers:
            for rock in self.rocks:
                offset_x = laser.x - rock.x
                offset_y = laser.y - rock.y
                if rock.surface.overlap(laser.surface, (offset_x, offset_y)):
                    laser.collided = True
                    rock.hp -= laser.damage
                    if rock.size == 2:
                        rock.update_middle_surface(self.images["middleRock100HP"])
                    elif rock.size == 3:
                        rock.update_big_surface(self.images["bigRock100HP"], self.images["bigRock200HP"])

    def adjust_game_phase(self):
        if self.score >= self.end_of_first_phase:
            self.game_phase = GamePhase.ALIENS

    def run(self):
        while self.running:
            self.clock.tick(30)

            if len(self.rocks) > 0:
                self.laser_rock_collisions()
                self.eliminate_rocks()
                self.spaceship_rock_collisions()

            self.eliminate_player()
            self.score += 0.2
            self.adjust_game_phase()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_screen_size(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.lasers.append(self.spaceship.shoot(self.images["laser"]))
                elif event.type == pygame.KEYDOWN:
                    for key, direction in self.key_to_attr.items():
                        if event.key == key:
                            self.spaceship.start_movement(direction)
                elif event.type == pygame.KEYUP:
                    for key, direction in self.key_to_attr.items():
                        if event.key == key:
                            self.spaceship.stop_movement(direction)

            self.spaceship.update_space_ship_coordinates(self.screen_width, self.screen_height)

            self.lasers = [laser for laser in self.lasers if not laser.above_screen() and not laser.collided]
            for laser in self.lasers:
                laser.update_laser_coordinates()

            if self.game_phase == GamePhase.ROCKS:
                self.spawn_rock()
            if len(self.rocks) > 0:
                self.rocks = [rock for rock in self.rocks if not rock.below_screen(self.screen_height)]
                for rock in self.rocks:
                    rock.update_rock_coordinates()

            self.reset_screen()
            self.draw_rocks()
            self.draw_lasers()
            self.draw_space_ship()

            hp_indicator = "Hp: " + str(self.spaceship.hp)
            self.draw_game_info((0, self.screen_height * 0.025), hp_indicator)
            score_counter = "Score: " + str(round(self.score))
            self.draw_game_info((self.screen_width, self.screen_height * 0.025), score_counter)

            pygame.display.update()
        pygame.quit()


def load_images() -> dict:
    """Loads every Picture once"""
    images = {
        'background': pygame.image.load('Background2.jpg'),
        'spaceship': pygame.image.load('SpaceShip.png'),
        'laser': pygame.image.load('laser.png'),
        'bigRock100HP': pygame.image.load('bigRock100HP.png'),
        'bigRock200HP': pygame.image.load('bigRock200HP.png'),
        'bigRock300HP': pygame.image.load('bigRock300HP.png'),
        'middleRock100HP': pygame.image.load('middleRock100HP.png'),
        'middleRock200HP': pygame.image.load('middleRock200HP.png'),
        'smallRock100HP': pygame.image.load('smallRock100HP.png'),
    }
    return images


app = App()
app.run()
