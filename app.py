import pygame
from pygame import Rect
from pygame.rect import RectType
from win32api import GetSystemMetrics

from Laser import Laser
from SpaceShip import SpaceShip


class App:
    def __init__(self):
        pygame.init()

        self.images = load_images()

        self.screen_width = GetSystemMetrics(0) * 0.25
        self.screen_height = GetSystemMetrics(1) * 0.6
        self.screen = self.initialize_screen()

        self.spaceship: SpaceShip = SpaceShip(self.screen_width, self.screen_height)
        self.spaceship_drawing: Rect | RectType = self.draw_space_ship()
        self.key_to_attr = {pygame.K_a: "moving_left",
                            pygame.K_w: "moving_up",
                            pygame.K_s: "moving_down",
                            pygame.K_d: "moving_right"}

        self.lasers: list[Laser] = []
        self.laser_drawings = self.draw_lasers()

        self.clock = pygame.time.Clock()

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

    def draw_space_ship(self):
        spaceship_picture = self.images["spaceship"]
        scaled_spaceship_picture = pygame.transform.scale(spaceship_picture,
                                                          (self.spaceship.width, self.spaceship.height))
        return self.screen.blit(scaled_spaceship_picture, (self.spaceship.x, self.spaceship.y))

    def draw_lasers(self):
        laser_picture = self.images["laser"]
        laser_drawings: list[Rect | RectType] = []
        for laser in self.lasers:
            scaled_spaceship_picture = pygame.transform.scale(laser_picture,
                                                              (laser.width, laser.height))
            laser_drawing = self.screen.blit(scaled_spaceship_picture, (laser.x, laser.y))
            laser_drawings.append(laser_drawing)
        return laser_drawings

    def run(self):
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_screen_size(event.w, event.h)
                elif event.type == pygame.KEYDOWN:
                    for key, attr_name in self.key_to_attr.items():
                        if event.key == key:
                            setattr(self.spaceship, attr_name, True)
                    if event.key == pygame.K_SPACE:
                        self.lasers.append(self.spaceship.shoot())
                elif event.type == pygame.KEYUP:
                    for key, attr_name in self.key_to_attr.items():
                        if event.key == key:
                            setattr(self.spaceship, attr_name, False)

            self.spaceship.update_space_ship_coordinates(self.screen_width, self.screen_height)

            self.lasers = [laser for laser in self.lasers if not laser.outside_screen()]
            for laser in self.lasers:
                laser.update_laser_coordinates()

            self.reset_screen()
            self.laser_drawings = self.draw_lasers()
            self.spaceship_drawing = self.draw_space_ship()
            pygame.display.update()
        pygame.quit()


def load_images() -> dict:
    """Loads every Picture once"""
    images = {
        'background': pygame.image.load('Background2.jpg'),
        'spaceship': pygame.image.load('SpaceShip.png'),
        'laser': pygame.image.load('laser.png')
    }
    return images


app = App()
app.run()
