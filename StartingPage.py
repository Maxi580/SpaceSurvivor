import sys
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


class StartingPage:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Space Survivor')

        self.images = load_images()
        pygame.display.set_icon(self.images['explosion2'])
        self.screen = self.initialize_screen()
        self.running = True

        self.play_button_x = 0
        self.play_button_y = 0
        self.play_button_width = 0
        self.play_button_height = 0

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

    def draw_game_info(self, pos: tuple[float, float], text: str, colours: tuple[tuple[int, int, int],
                       tuple[int, int, int]], font_size):
        """Lädt einen Text, wendet darauf einen Farbverlauf an und zeichnet ihn."""
        font = pygame.font.SysFont('Raleway Bold', font_size)
        surface = font.render(text, True, (0, 0, 0))

        utils.apply_vertical_gradient(surface, colours[0], colours[1])

        if pos[0] <= 0:
            x = pos[0] + self.screen.get_width() * 0.0025
        elif pos[0] >= self.screen.get_width():
            x = self.screen.get_width() * 0.9975 - surface.get_width()
        else:
            x = pos[0] - surface.get_width() * 0.5

        self.screen.blit(surface, (x, pos[1]))

    def draw_button(self, x: float, y: float, width: float, height: float, text: str, font_size: int,
                    text_color: tuple[tuple[int, int, int], tuple[int, int, int]],
                    rect_color: tuple[int, int, int, int]):
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
        x = self.screen.get_width() * 0.5
        y = self.screen.get_height() * 0.1
        start_color = (0, 255, 0)
        end_color = (0, 128, 0)
        font_size = int(0.1 * self.screen.get_width())
        self.draw_game_info((x, y), title, (start_color, end_color), font_size)

        text = "Play!"
        width = self.screen.get_width() * 0.4
        height = self.screen.get_height() * 0.1
        play_button_x = self.screen.get_width() * 0.5 - width * 0.5
        play_button_y = self.screen.get_height() * 0.2
        self.draw_button(play_button_x, play_button_y, width, height, text, font_size,
                         (start_color, end_color), (0, 0, 0, 210))
        self.play_button_x = play_button_x
        self.play_button_y = play_button_y
        self.play_button_width = width
        self.play_button_height = height

        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.draw_overlay()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if self.play_button_x <= mouse_x <= (self.play_button_x + self.play_button_width) and \
                            self.play_button_y <= mouse_y <= (self.play_button_y + self.play_button_height):
                        app = App(self.images, self.screen)
                        app.run()

            self.reset_screen()
            self.draw_overlay()
            pygame.display.update()


starting_page = StartingPage()
starting_page.run()
