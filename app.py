import random
from enum import Enum, auto

import pygame
import pygame.freetype
from win32api import GetSystemMetrics

from Alien import Alien
from Explosion import Explosion
from Laser import Laser
from Rock import Rock
from SpaceShip import SpaceShip


class GamePhase(Enum):
    ROCKS = auto()
    ALIENS = auto()
    BASE = auto()


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
        self.alien_lasers: list[Laser] = []

        self.rocks: list[Rock] = []
        self.rock_spawn_start_probability = 0.0025
        self.rock_spawn_increment_probability = 0.0025
        self.rock_spawn_probability = self.rock_spawn_start_probability

        self.aliens: list[Alien] = []

        self.explosions: list[Explosion] = []

        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.ROCKS
        self.end_of_first_phase = 100
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
        for alien in self.aliens:
            alien.adjust_size_to_window_resize(self.screen_width, self.screen_height, width, height)

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

    def trigger_explosion(self, space_ship_x, space_ship_y, space_ship_width, space_ship_height,
                          size_factor: float = 1, colliding_rock: Rock = None, colliding_spaceship: SpaceShip = None):
        self.explosions.append(Explosion(space_ship_x, space_ship_y, space_ship_width, space_ship_height,
                                         self.images['explosion1'], size_factor, colliding_rock, colliding_spaceship))

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

    def draw_object(self, draw_object):
        scaled_object_picture = pygame.transform.scale(draw_object.picture, (draw_object.width, draw_object.height))
        if isinstance(draw_object, SpaceShip) or isinstance(draw_object, Rock) or isinstance(draw_object, Laser) \
                or isinstance(draw_object, Alien):
            draw_object.surface = pygame.mask.from_surface(scaled_object_picture)
        self.screen.blit(scaled_object_picture, (draw_object.x, draw_object.y))

    def eliminate_player(self):
        if self.spaceship.hp <= 0:
            print("Lost")
            self.running = False
            pygame.quit()

    def spawn_aliens(self):
        y = self.screen_height * 0.1
        self.aliens.append(Alien(0, y, self.screen_width, self.screen_height,
                                 self.images["alien_spaceship"]))
        self.aliens.append(Alien(self.screen_width * 0.25, y, self.screen_width,
                                 self.screen_height, self.images["alien_spaceship"]))
        self.aliens.append(Alien(self.screen_width * 0.5, y, self.screen_width,
                                 self.screen_height, self.images["alien_spaceship"]))
        self.aliens.append(Alien(self.screen_width * 0.75, y, self.screen_width,
                                 self.screen_height, self.images["alien_spaceship"]))
        self.aliens.append(Alien(self.screen_width, y, self.screen_width, self.screen_height,
                                 self.images["alien_spaceship"]))

    def eliminate_objects(self, killable_objects):
        i = 0
        while i < len(killable_objects):
            if killable_objects[i].hp <= 0:
                if isinstance(killable_objects[i], Alien):
                    self.trigger_explosion(killable_objects[i].x, killable_objects[i].y, killable_objects[i].width,
                                           killable_objects[i].height, 1.2)
                elif isinstance(killable_objects[i], Rock):
                    self.trigger_explosion(killable_objects[i].x, killable_objects[i].y, killable_objects[i].width,
                                           killable_objects[i].height, 0.7)

                killable_objects.pop(i)
            else:
                i += 1

    def alien_shoot(self):
        for alien in self.aliens:
            if random.random() < 0.035:
                self.alien_lasers.append(Laser(alien.x, alien.y, alien.width, alien.height,
                                               alien.calculate_shot_velocity(self.spaceship.x, self.spaceship.y),
                                               self.images['alien_laser']))

    def space_ship_collisions(self, colliders):
        for collider in colliders:
            offset_x = self.spaceship.x - collider.x
            offset_y = self.spaceship.y - collider.y
            if collider.surface.overlap(self.spaceship.surface, (offset_x, offset_y)):
                if not self.spaceship.immune:
                    self.spaceship.hp -= collider.damage
                    self.spaceship.set_immune()
                if isinstance(collider, Laser):
                    collider.collided = True
                    self.trigger_explosion(self.spaceship.x, self.spaceship.y, self.spaceship.width,
                                           self.spaceship.height)
                elif isinstance(collider, Rock):
                    self.trigger_explosion(self.spaceship.x, self.spaceship.y, self.spaceship.width,
                                           self.spaceship.height, colliding_spaceship=self.spaceship)
                    collider.hp = 0

    def non_space_ship_collisions(self, colliders1, colliders2):
        for collider1 in colliders1:
            for collider2 in colliders2:
                offset_x = collider1.x - collider2.x
                offset_y = collider1.y - collider2.y
                if collider2.surface.overlap(collider1.surface, (offset_x, offset_y)):
                    if isinstance(collider1, Laser) and isinstance(collider2, Alien):
                        self.trigger_explosion(collider1.x, collider1.y, collider1.width * 2, collider1.width * 2,
                                               1)
                        collider1.collided = True
                        collider2.hp -= collider1.damage
                    if isinstance(collider1, Laser) and isinstance(collider2, Rock):
                        self.trigger_explosion(collider1.x, collider1.y, collider1.width * 2, collider1.width * 2,
                                               1, collider2)
                        collider1.collided = True
                        collider2.hp -= collider1.damage
                        if collider2.size == 2:
                            collider2.update_middle_surface(self.images["middleRock100HP"])
                        elif collider2.size == 3:
                            collider2.update_big_surface(self.images["bigRock100HP"], self.images["bigRock200HP"])

    def adjust_game_phase(self):
        if self.game_phase == GamePhase.ROCKS and self.score >= self.end_of_first_phase:
            self.game_phase = GamePhase.ALIENS

    def run(self):
        while self.running:
            self.clock.tick(30)

            if len(self.rocks) > 0:
                self.non_space_ship_collisions(self.lasers, self.rocks)
                self.eliminate_objects(self.rocks)
                self.space_ship_collisions(self.rocks)

            if len(self.aliens) > 0:
                self.non_space_ship_collisions(self.lasers, self.aliens)
                self.eliminate_objects(self.aliens)
                self.alien_shoot()

            if len(self.alien_lasers) > 0:
                self.space_ship_collisions(self.alien_lasers)

            for explosion in self.explosions:
                explosion.age += 1
                if explosion.adjust_stage_to_age() and explosion.stage <= 8:
                    explosion.adjust_picture_to_stage(self.images['explosion' + str(explosion.stage)])
            self.explosions = [explosion for explosion in self.explosions if explosion.stage <= 8]

            if self.spaceship.immune:
                self.spaceship.increase_immune_counter()
            self.spaceship.reset_immune()

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
            self.alien_lasers = [alien_laser for alien_laser in self.alien_lasers if not
                                 alien_laser.below_screen(self.screen_height) and not alien_laser.collided]

            for laser in self.lasers:
                laser.update_laser_coordinates()
            for alien_laser in self.alien_lasers:
                alien_laser.update_laser_coordinates()

            if self.game_phase == GamePhase.ROCKS:
                self.spawn_rock()
            if len(self.rocks) > 0:
                self.rocks = [rock for rock in self.rocks if not rock.below_screen(self.screen_height)]
                for rock in self.rocks:
                    rock.update_rock_coordinates()

            if self.game_phase == GamePhase.ALIENS and len(self.rocks) == 0:
                self.game_phase = GamePhase.BASE
                self.spawn_aliens()

            self.reset_screen()
            for rock in self.rocks:
                self.draw_object(rock)
            for laser in self.lasers:
                self.draw_object(laser)
            for alien_laser in self.alien_lasers:
                self.draw_object(alien_laser)
            for alien in self.aliens:
                self.draw_object(alien)
            self.draw_object(self.spaceship)
            for explosion in self.explosions:
                if explosion.colliding_rock:
                    explosion.adjust_y_to_movement_of_object()
                if explosion.colliding_spaceship:
                    explosion.adjust_coordinates_to_spaceship()
                self.draw_object(explosion)

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
        'alien_spaceship': pygame.image.load('AlienSpaceShip.png'),
        'laser': pygame.image.load('laser.png'),
        'alien_laser': pygame.image.load('AlienLaser.png'),
        'bigRock100HP': pygame.image.load('bigRock100HP.png'),
        'bigRock200HP': pygame.image.load('bigRock200HP.png'),
        'bigRock300HP': pygame.image.load('bigRock300HP.png'),
        'middleRock100HP': pygame.image.load('middleRock100HP.png'),
        'middleRock200HP': pygame.image.load('middleRock200HP.png'),
        'smallRock100HP': pygame.image.load('smallRock100HP.png'),
        'explosion1': pygame.image.load('explosion1.png'),
        'explosion2': pygame.image.load('explosion2.png'),
        'explosion3': pygame.image.load('explosion3.png'),
        'explosion4': pygame.image.load('explosion4.png'),
        'explosion5': pygame.image.load('explosion5.png'),
        'explosion6': pygame.image.load('explosion6.png'),
        'explosion7': pygame.image.load('explosion7.png'),
        'explosion8': pygame.image.load('explosion8.png'),
    }
    return images


app = App()
app.run()
