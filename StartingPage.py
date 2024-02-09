import sys
from enum import Enum, auto

import utils

import pygame
import pygame.freetype
from win32api import GetSystemMetrics

from app import App


def load_images() -> dict:
    """Loads every Picture once"""
    images = {
        'background': pygame.image.load('resources/Background2.jpg'),
        'spaceship': pygame.image.load('resources/SpaceShip.png'),
        'alien_spaceship': pygame.image.load('resources/AlienSpaceShip.png'),
        'laser': pygame.image.load('resources/laser.png'),
        'alien_laser': pygame.image.load('resources/AlienLaser.png'),
        'bigRock100HP': pygame.image.load('resources/bigRock100HP.png'),
        'bigRock200HP': pygame.image.load('resources/bigRock200HP.png'),
        'bigRock300HP': pygame.image.load('resources/bigRock300HP.png'),
        'middleRock100HP': pygame.image.load('resources/middleRock100HP.png'),
        'middleRock200HP': pygame.image.load('resources/middleRock200HP.png'),
        'smallRock100HP': pygame.image.load('resources/smallRock100HP.png'),
        'explosion1': pygame.image.load('resources/explosion1.png'),
        'explosion2': pygame.image.load('resources/explosion2.png'),
        'explosion3': pygame.image.load('resources/explosion3.png'),
        'explosion4': pygame.image.load('resources/explosion4.png'),
        'explosion5': pygame.image.load('resources/explosion5.png'),
        'explosion6': pygame.image.load('resources/explosion6.png'),
        'explosion7': pygame.image.load('resources/explosion7.png'),
        'explosion8': pygame.image.load('resources/explosion8.png'),
        'meteoroid': pygame.image.load('resources/meteoroid.png'),
        'shield': pygame.image.load('resources/Shield.png'),
    }
    return images


class Difficulty(Enum):
    EASY = 150
    NORMAL = 100
    HARD = 50


class StartingPage:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Space Survivor')
        self.clock = pygame.time.Clock()

        self.images = load_images()
        pygame.display.set_icon(self.images['explosion2'])
        self.screen = self.initialize_screen()
        self.old_width = self.screen.get_width()
        self.old_height = self.screen.get_height()
        self.running = True
        self.game_difficulty = Difficulty.NORMAL

        self.green_colors = [(0, 255, 0), (0, 128, 0)]
        self.grey_colors = [(64, 64, 64), (128, 128, 128)]
        self.font_size = int(0.1 * self.screen.get_width())

        self.headline_width = self.screen.get_width() * 0.4
        self.headline_height = self.screen.get_height() * 0.1
        self.headline_x = self.screen.get_width() * 0.5
        self.headline_y = self.screen.get_height() * 0.1

        self.play_button_width = self.screen.get_width() * 0.5
        self.play_button_height = self.screen.get_height() * 0.1
        self.play_button_x = self.screen.get_width() * 0.5 - self.play_button_width * 0.5
        self.play_button_y = self.screen.get_height() * 0.3

        self.difficulty_button_width = self.screen.get_width() * 0.15
        self.difficulty_button_height = self.screen.get_height() * 0.05
        self.difficulty_button_y = self.play_button_y * 1.05 + self.play_button_height
        self.difficulty_button_distance = self.screen.get_width() * 0.025

        self.easy_button_x = self.play_button_x
        self.normal_button_x = self.play_button_x + self.difficulty_button_width + self.difficulty_button_distance
        self.hard_button_x = self.play_button_x + 2 * self.difficulty_button_width + 2 * self.difficulty_button_distance

    def initialize_screen(self):
        width = GetSystemMetrics(0) * 0.25
        height = GetSystemMetrics(1) * 0.6

        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        background = self.images["background"]
        scaled_background = pygame.transform.scale(background, (width, height))
        screen.blit(scaled_background, (0, 0))
        pygame.display.update()

        return screen

    def reset_screen(self):
        background = self.images["background"]
        scaled_background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(scaled_background, (0, 0))

    def adjust_values_to_resize(self):
        width_values = ['headline_width', 'headline_x', 'play_button_width', 'play_button_x', 'difficulty_button_width',
                        'easy_button_x', 'normal_button_x', 'hard_button_x']

        for width_value in width_values:
            current_value = getattr(self, width_value)
            new_value = current_value * self.screen.get_width() / self.old_width
            setattr(self, width_value, new_value)

        height_values = ['headline_height', 'headline_y', 'play_button_height', 'play_button_y',
                         'difficulty_button_height', 'difficulty_button_y']
        for height_value in height_values:
            current_value = getattr(self, height_value)
            new_value = current_value * self.screen.get_height() / self.old_height
            setattr(self, height_value, new_value)

        self.font_size = int(self.font_size * (self.screen.get_width() / self.old_width))
        self.old_width = self.screen.get_width()
        self.old_height = self.screen.get_height()

    def draw_game_info(self, pos: tuple[float, float], text: str, colours: tuple[tuple[int, int, int],
                       tuple[int, int, int]]):
        """Lädt einen Text, wendet darauf einen Farbverlauf an und zeichnet ihn."""
        font = pygame.font.SysFont('Raleway Bold', self.font_size)
        surface = font.render(text, True, (0, 0, 0))

        utils.apply_vertical_gradient(surface, colours[0], colours[1])

        self.screen.blit(surface, (pos[0] - (surface.get_width() * 0.5), pos[1]))

    def draw_button(self, x: float, y: float, width: float, height: float, text: str,
                    text_color: tuple[tuple[int, int, int], tuple[int, int, int]],
                    rect_color: tuple[int, int, int, int], font_size):
        font = pygame.font.SysFont('Raleway Bold', font_size)
        font_surf = font.render(text, True, (0, 0, 0))
        utils.apply_vertical_gradient(font_surf, text_color[0], text_color[1])
        rect_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surf, rect_color, rect_surf.get_rect())

        rect_surf.blit(font_surf, ((width / 2) - (font_surf.get_width() * 0.5),
                                   (height / 2) - (font_surf.get_height() * 0.5)))

        self.screen.blit(rect_surf, (x, y))

    def draw_overlay(self):
        title = "Welcome to Space Survivor!"
        self.draw_game_info((self.headline_x, self.headline_y), title,
                            (self.green_colors[0], self.green_colors[1]))

        text = "Play!"
        self.draw_button(self.play_button_x, self.play_button_y, self.play_button_width, self.play_button_height,
                         text, (self.green_colors[0], self.green_colors[1]),
                         (0, 0, 0, 210), self.font_size)

        text = "Easy"
        if self.game_difficulty == Difficulty.EASY:
            start_color, end_color = self.green_colors[0], self.green_colors[1]
        else:
            start_color, end_color = self.grey_colors[0], self.grey_colors[1]
        self.draw_button(self.easy_button_x, self.difficulty_button_y, self.difficulty_button_width,
                         self.difficulty_button_height, text,(start_color, end_color),
                         (0, 0, 0, 210), self.font_size//2)

        text = "Normal"
        if self.game_difficulty == Difficulty.NORMAL:
            start_color, end_color = self.green_colors[0], self.green_colors[1]
        else:
            start_color, end_color = self.grey_colors[0], self.grey_colors[1]
        self.draw_button(self.normal_button_x, self.difficulty_button_y, self.difficulty_button_width,
                         self.difficulty_button_height, text, (start_color, end_color),(0, 0, 0, 210),
                         self.font_size//2)
        text = "Hard"
        if self.game_difficulty == Difficulty.HARD:
            start_color, end_color = self.green_colors[0], self.green_colors[1]
        else:
            start_color, end_color = self.grey_colors[0], self.grey_colors[1]
        self.draw_button(self.hard_button_x, self.difficulty_button_y, self.difficulty_button_width,
                         self.difficulty_button_height, text, (start_color, end_color), (0, 0, 0, 210),
                         self.font_size//2)

        pygame.display.update()

    def run(self):
        self.reset_screen()
        self.draw_overlay()
        while self.running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.adjust_values_to_resize()
                    self.reset_screen()
                    self.draw_overlay()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if self.play_button_x <= mouse_x <= (self.play_button_x + self.play_button_width) and \
                            self.play_button_y <= mouse_y <= (self.play_button_y + self.play_button_height):
                        app = App(self.images, self.screen, self.game_difficulty.value)
                        app.run()
                    elif self.easy_button_x <= mouse_x <= (self.easy_button_x + self.difficulty_button_width) and \
                            self.difficulty_button_y <= mouse_y <= (self.difficulty_button_y +
                                                                    self.difficulty_button_height):
                        self.game_difficulty = Difficulty.EASY
                    elif self.normal_button_x <= mouse_x <= (self.normal_button_x + self.difficulty_button_width) and \
                            self.difficulty_button_y <= mouse_y <= (self.difficulty_button_y +
                                                                    self.difficulty_button_height):
                        self.game_difficulty = Difficulty.NORMAL
                    elif self.hard_button_x <= mouse_x <= (self.hard_button_x + self.difficulty_button_width) and \
                            self.difficulty_button_y <= mouse_y <= (self.difficulty_button_y +
                                                                    self.difficulty_button_height):
                        self.game_difficulty = Difficulty.HARD

                    self.reset_screen()
                    self.draw_overlay()

            pygame.display.update()


starting_page = StartingPage()
starting_page.run()