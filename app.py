import math
import random
import sys
from enum import Enum, auto

from pygame import Surface, SurfaceType

import utils

import pygame
import pygame.freetype

from Alien import Alien
from Explosion import Explosion
from Laser import Laser
from Meteoroid import Meteoroid
from Mothership import Mothership
from Observer import WindowResizeSubject, ResizeObserver
from Rock import Rock
from Rocket import Rocket
from SpaceShip import SpaceShip

ROCK_PROBABILITY = 0.0025
METEOROID_GAP_FACTOR = 1.17
ROCK_PHASE_SPAWNED_ROCKS = 0
METEOROID_PHASE_HAIL_AMOUNT = 3
ALIEN_SHOOT_PROBABILITY = 0.035
ROCKETS_AMOUNT = 10


SHIP_BASE_VELOCITY = 7
LASER_BASE_VELOCITY = 9
ROCK_BASE_VELOCITY = 9
METEOROID_BASE_VELOCITY = 6
ROCKET_BASE_VELOCITY = 6


class GamePhase(Enum):
    ROCKS = auto()
    ALIENS = auto()
    FIGHTING_ALIENS = auto()
    METEOROIDS = auto()
    ROCKETS = auto()


class App:
    def __init__(self, images: dict, screen: Surface | SurfaceType, hp: int, difficulty_factor: int):
        self.images = images

        self.screen = screen
        self.old_width = screen.get_width()
        self.old_height = screen.get_height()
        self.resize_subject = WindowResizeSubject()

        self.green_color = [(0, 255, 0), (0, 128, 0)]
        self.red_color = [(255, 0, 0), (102, 0, 0)]
        self.font_size = int(0.1 * self.screen.get_width())

        self.difficulty_factor = difficulty_factor
        self.ship_hp = hp
        self.ship_velocity = SHIP_BASE_VELOCITY * difficulty_factor
        self.laser_velocity = LASER_BASE_VELOCITY * difficulty_factor
        self.rock_velocity = ROCK_BASE_VELOCITY * difficulty_factor
        self.meteoroid_velocity = METEOROID_BASE_VELOCITY * difficulty_factor

        self.spaceship: SpaceShip = SpaceShip(self.screen.get_width(), self.screen.get_height(),
                                              self.images['spaceship'], hp, self.ship_velocity,
                                              self.laser_velocity)
        self.initialize_observer(self.spaceship, self.screen.get_width(), self.screen.get_height())

        self.key_to_attr = {pygame.K_a: 'LEFT',
                            pygame.K_w: 'UP',
                            pygame.K_s: 'DOWN',
                            pygame.K_d: 'RIGHT'}

        self.lasers: list[Laser] = []
        self.alien_lasers: list[Laser] = []

        self.rocks: list[Rock] = []
        self.rock_spawn_start_probability = ROCK_PROBABILITY
        self.rock_spawn_increment_probability = ROCK_PROBABILITY
        self.rock_spawn_probability = self.rock_spawn_start_probability
        self.rock_stage_velocity_factor = 1

        self.aliens: list[Alien] = []
        self.explosions: list[Explosion] = []

        self.meteoroids: list[Meteoroid] = []
        self.meteoroid_gap_factor = METEOROID_GAP_FACTOR
        self.meteoroid_hail_counter = 0
        self.meteoroid_phase_hail_amount = METEOROID_PHASE_HAIL_AMOUNT

        self.rockets: list[Rocket] = []
        self.rocket_x = self.screen.get_width() // 2
        self.rocket_y = 0
        self.rocket_velocity = ROCKET_BASE_VELOCITY * difficulty_factor
        self.rocket_amount = ROCKETS_AMOUNT * difficulty_factor

        self.mothership: Mothership = Mothership(self.screen.get_width(), self.screen.get_height(),
                                                 self.images['alien_spaceship'])

        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.ROCKS
        self.rock_counter = 0
        self.rock_phase_spawned_rocks = ROCK_PHASE_SPAWNED_ROCKS
        self.score = 0
        self.running = True

    def reset_screen(self):
        background = self.images["background"]
        scaled_background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(scaled_background, (0, 0))

    def initialize_observer(self, entity, screen_width: int, screen_height: int):
        resize_observer = ResizeObserver(entity, screen_width, screen_height)
        self.resize_subject.attach(resize_observer)

    def draw_game_info(self, pos: tuple[float, float], text: str, colours: tuple[tuple[int, int, int],
                       tuple[int, int, int]]):
        """Lädt einen Text, wendet darauf einen Farbverlauf an und zeichnet ihn."""
        font = pygame.font.SysFont('Raleway Bold', self.font_size)
        surface = font.render(text, True, (0, 0, 0))

        utils.apply_vertical_gradient(surface, colours[0], colours[1])

        if pos[0] <= 0:
            x = pos[0] + self.screen.get_width() * 0.0025
        elif pos[0] >= self.screen.get_width():
            x = self.screen.get_width() * 0.9975 - surface.get_width()
        else:
            x = pos[0] - surface.get_width() * 0.5

        self.screen.blit(surface, (x, pos[1]))

    def trigger_explosion(self, x, y, width, height,
                          size_factor: float = 1, colliding_rock: Rock = None, colliding_spaceship: SpaceShip = None):
        self.explosions.append(Explosion(x, y, width, height,
                                         self.images['explosion1'], size_factor, colliding_rock, colliding_spaceship))
        self.initialize_observer(self.explosions[-1], self.screen.get_width(), self.screen.get_height())

    def create_rock(self, x, size):
        surfaces = [self.images["smallRock100HP"], self.images["middleRock200HP"], self.images["bigRock300HP"]]
        return Rock(x, self.screen.get_width(), self.screen.get_height(), size, surfaces[size - 1],
                    self.rock_velocity - (self.rock_stage_velocity_factor * size), self.ship_hp)

    def spawn_rock(self):
        if random.random() < self.rock_spawn_probability:
            random_size_number = random.random()
            if random_size_number <= 0.35:
                new_rock = self.create_rock(random.randint(0, self.screen.get_width()), 1)
            elif random_size_number <= 0.75:
                new_rock = self.create_rock(random.randint(0, self.screen.get_width()), 2)
            else:
                new_rock = self.create_rock(random.randint(0, self.screen.get_width()), 3)
            self.rocks.append(new_rock)
            self.initialize_observer(new_rock, self.screen.get_width(), self.screen.get_height())
            self.rock_counter += 1
            self.rock_spawn_probability = self.rock_spawn_start_probability
        else:
            self.rock_spawn_probability += self.rock_spawn_increment_probability

    def draw_object(self, draw_object):
        self.screen.blit(draw_object.picture, (draw_object.x, draw_object.y))

    def draw_spaceship_shield(self):
        if self.spaceship.is_immune() and self.spaceship.get_hp() > 0:
            if self.spaceship.get_immune_counter() < 75 or self.spaceship.get_immune_counter() % 4 == 0:
                scaled_shield_picture = pygame.transform.scale(self.images['shield'],
                                                               (self.spaceship.get_width() * 1.4,
                                                                self.spaceship.get_height() * 1.4))
                self.screen.blit(scaled_shield_picture, (self.spaceship.get_x() - 0.2 * self.spaceship.get_width(),
                                                         self.spaceship.get_y() - 0.2 * self.spaceship.get_height()))

    def draw_health_bar(self, alien: Alien):
        red = (255, 0, 0)
        green = (0, 255, 0)

        health_ratio = alien.get_hp() / alien.get_max_hp()
        length = alien.get_width()
        height = self.screen.get_height() * 0.02

        current_bar_length = length * health_ratio
        x = alien.get_x()
        y = alien.get_height() + alien.get_y() + self.screen.get_height() * 0.01

        pygame.draw.rect(self.screen, red, (x, y, length, height))
        pygame.draw.rect(self.screen, green, (x, y, current_bar_length, height))

    def eliminate_player(self):
        if self.spaceship.get_hp() <= 0:
            self.running = False
            self.end_of_game()

    def spawn_aliens(self):
        self.aliens.append(Alien(0, self.screen.get_width(), self.screen.get_height(),
                                 self.images["alien_spaceship"], self.ship_velocity, self.laser_velocity,
                                 self.ship_hp))
        self.aliens.append(Alien(self.screen.get_width() * 0.25, self.screen.get_width(),
                                 self.screen.get_height(), self.images["alien_spaceship"], self.ship_velocity,
                                 self.laser_velocity, self.ship_hp))
        self.aliens.append(Alien(self.screen.get_width() * 0.5, self.screen.get_width(),
                                 self.screen.get_height(), self.images["alien_spaceship"], self.ship_velocity,
                                 self.laser_velocity, self.ship_hp))
        self.aliens.append(Alien(self.screen.get_width() * 0.75, self.screen.get_width(),
                                 self.screen.get_height(), self.images["alien_spaceship"], self.ship_velocity,
                                 self.laser_velocity, self.ship_hp))
        self.aliens.append(Alien(self.screen.get_width(), self.screen.get_width(), self.screen.get_height(),
                                 self.images["alien_spaceship"], self.ship_velocity,
                                 self.laser_velocity, self.ship_hp))
        for alien in self.aliens:
            self.initialize_observer(alien, self.screen.get_width(), self.screen.get_height())

    def eliminate_objects(self, killable_objects):
        i = 0
        while i < len(killable_objects):
            if killable_objects[i].hp <= 0:
                if isinstance(killable_objects[i], Alien) or isinstance(killable_objects[i], Meteoroid) \
                        or isinstance(killable_objects[i], Rocket):
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
            if random.random() < ALIEN_SHOOT_PROBABILITY:
                self.alien_lasers.append(Laser(alien.get_x(), alien.get_y(), alien.get_width(), alien.get_height(),
                                               alien.calculate_shot_velocity(self.spaceship.get_x(),
                                                                             self.spaceship.get_y()),
                                               self.images['alien_laser']))
                self.initialize_observer(self.alien_lasers[-1], self.screen.get_width(), self.screen.get_height())

    def spawn_meteoroid_hail(self):
        pos1 = random.randint(0,
                              int(self.screen.get_width() - (self.spaceship.get_width() * self.meteoroid_gap_factor)))
        pos2 = pos1 + self.spaceship.get_width() * self.meteoroid_gap_factor
        width = self.screen.get_width() / 6
        while pos2 < self.screen.get_width():
            self.meteoroids.append(Meteoroid(pos2, width, self.screen.get_height(), self.images['meteoroid'],
                                             self.meteoroid_velocity))
            pos2 += width

        while pos1 > -width:
            self.meteoroids.append(Meteoroid(pos1 - width, width, self.screen.get_height(), self.images['meteoroid'],
                                             self.meteoroid_velocity))
            pos1 -= width

        for meteoroid in self.meteoroids:
            self.initialize_observer(meteoroid, self.screen.get_width(), self.screen.get_height())

    def spawn_rockets(self):
        if len(self.rockets) < self.rocket_amount:
            self.rockets.append(Rocket(self.rocket_velocity, self.mothership.get_width(), self.mothership.get_height(),
                                       self.mothership.get_x(), self.mothership.get_y(), self.images['rocket']))
            self.initialize_observer(self.rockets[-1], self.screen.get_width(), self.screen.get_height())

    def space_ship_collisions(self, colliders):
        for collider in colliders:
            offset_x = self.spaceship.get_x() - collider.x
            offset_y = self.spaceship.get_y() - collider.y
            if collider.surface.overlap(self.spaceship.surface, (offset_x, offset_y)):
                if not self.spaceship.immune:
                    self.spaceship.reduce_hp(collider.damage)
                    self.spaceship.set_immune()
                if isinstance(collider, Laser):
                    collider.collided = True
                elif isinstance(collider, Rock) or isinstance(collider, Meteoroid) or isinstance(collider, Rocket):
                    collider.hp = 0
                self.trigger_explosion(self.spaceship.get_x(), self.spaceship.get_y(), self.spaceship.get_width(),
                                       self.spaceship.get_height(), colliding_spaceship=self.spaceship)

    def non_space_ship_collisions(self, colliders1, colliders2):
        for collider1 in colliders1:
            for collider2 in colliders2:
                offset_x = collider1.x - collider2.x
                offset_y = collider1.y - collider2.y
                if collider2.surface.overlap(collider1.surface, (offset_x, offset_y)):
                    collider1.collided = True
                    if isinstance(collider2, Alien):
                        self.trigger_explosion(collider1.x, collider1.y, collider1.width * 2, collider1.width * 2,
                                               1)

                        collider2.hp -= collider1.damage
                    if isinstance(collider2, Rock):
                        self.trigger_explosion(collider1.x, collider1.y, collider1.width * 2, collider1.width * 2,
                                               1, collider2)
                        collider2.hp -= collider1.damage
                        if collider2.size == 2:
                            collider2.update_middle_surface(self.images["middleRock100HP"])
                        elif collider2.size == 3:
                            collider2.update_big_surface(self.images["bigRock100HP"], self.images["bigRock200HP"])

    def run(self):
        while self.running:
            self.clock.tick(30)

            # Detect Collisions and Eliminate Objects without HP
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

            if len(self.meteoroids) > 0:
                self.space_ship_collisions(self.meteoroids)
                self.non_space_ship_collisions(self.lasers, self.meteoroids)
                self.eliminate_objects(self.meteoroids)

            if len(self.rockets) > 0:
                self.space_ship_collisions(self.rockets)
                self.eliminate_objects(self.rockets)

            self.lasers = [laser for laser in self.lasers if not laser.above_screen() and not laser.get_collided()]
            self.alien_lasers = [alien_laser for alien_laser in self.alien_lasers
                                 if not alien_laser.below_screen(self.screen.get_height())
                                 and not alien_laser.get_collided()]
            self.rocks = [rock for rock in self.rocks
                          if not rock.below_screen(self.screen.get_height())]
            self.meteoroids = [meteoroid for meteoroid in self.meteoroids
                               if not meteoroid.below_screen(self.screen.get_height())]

            # Update the coordinates of remaining objects according to velocity, also handle explosion animation
            self.spaceship.update_coordinates(self.screen.get_width(), self.screen.get_height())
            for alien in self.aliens:
                alien.update_coordinates(self.screen.get_height() * 0.1)
            for laser in self.lasers:
                laser.update_coordinates()
            for alien_laser in self.alien_lasers:
                alien_laser.update_coordinates()
            for rock in self.rocks:
                rock.update_coordinates()
            for explosion in self.explosions:
                explosion.increase_age(1)
                if explosion.adjust_stage_to_age() and explosion.get_stage() <= 8:
                    explosion.adjust_picture_to_stage(self.images['explosion' + str(explosion.get_stage())])
            self.explosions = [explosion for explosion in self.explosions if explosion.get_stage() <= 8]
            for meteoroid in self.meteoroids:
                meteoroid.update_coordinates()
            for rocket in self.rockets:
                rocket.update_coordinates(self.screen.get_width(), self.screen.get_height())
                rocket.return_at_border(self.screen.get_width(), self.screen.get_height())

            # After a Player took Damage he is immune for a short period of time
            if self.spaceship.is_immune():
                self.spaceship.increase_immune_counter()
            self.spaceship.reset_immune()

            #  Close the Game if a player is dead, raise score if he is not
            self.eliminate_player()
            self.score += 0.2 * self.difficulty_factor

            # Catch User Input for shooting, movement, window-resize and quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.resize_subject.notify(event)
                    self.old_width = self.screen.get_width()
                    self.old_height = self.screen.get_height()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_phase != GamePhase.ROCKETS:
                    self.lasers.append(self.spaceship.shoot(self.images["laser"]))
                    self.initialize_observer(self.lasers[-1], self.screen.get_width(), self.screen.get_height())
                elif event.type == pygame.KEYDOWN:
                    for key, direction in self.key_to_attr.items():
                        if event.key == key:
                            self.spaceship.start_movement(direction)
                elif event.type == pygame.KEYUP:
                    for key, direction in self.key_to_attr.items():
                        if event.key == key:
                            self.spaceship.stop_movement(direction)

            # Handle Game-Phases
            if self.game_phase == GamePhase.ROCKS:
                self.spawn_rock()

            if self.game_phase == GamePhase.ROCKS and self.rock_counter >= self.rock_phase_spawned_rocks:
                self.game_phase = GamePhase.ALIENS

            if self.game_phase == GamePhase.ALIENS and len(self.rocks) == 0:
                self.game_phase = GamePhase.FIGHTING_ALIENS
                self.spawn_aliens()

            if self.game_phase == GamePhase.FIGHTING_ALIENS and len(self.aliens) == 0 and len(self.alien_lasers) == 0:
                self.game_phase = GamePhase.METEOROIDS

            if self.game_phase == GamePhase.METEOROIDS and len(self.meteoroids) == 0:
                self.spawn_meteoroid_hail()
                self.meteoroid_hail_counter += 1
                if self.meteoroid_hail_counter >= self.meteoroid_phase_hail_amount:
                    self.game_phase = GamePhase.ROCKETS

            if self.game_phase == GamePhase.ROCKETS and len(self.meteoroids) == 0:
                self.spawn_rockets()

            # Draw everything
            self.reset_screen()
            for rock in self.rocks:
                self.draw_object(rock)
            for laser in self.lasers:
                self.draw_object(laser)
            for alien_laser in self.alien_lasers:
                self.draw_object(alien_laser)
            for alien in self.aliens:
                self.draw_object(alien)
                self.draw_health_bar(alien)
            for meteoroid in self.meteoroids:
                self.draw_object(meteoroid)
            for rocket in self.rockets:
                self.draw_object(rocket)
            if self.game_phase == GamePhase.ROCKETS and len(self.meteoroids) == 0:
                self.draw_object(self.mothership)
            self.draw_object(self.spaceship)
            self.draw_spaceship_shield()
            for explosion in self.explosions:
                if explosion.get_colliding_rock():
                    explosion.adjust_y_to_movement_of_object()
                if explosion.get_colliding_spaceship():
                    explosion.adjust_coordinates_to_spaceship()
                self.draw_object(explosion)

            hp_indicator = "Hp: " + str(self.spaceship.get_hp())
            self.draw_game_info((0, self.screen.get_height() * 0.025), hp_indicator,
                                (self.green_color[0], self.green_color[1]))
            score_counter = "Score: " + str(int(self.score))
            self.draw_game_info((self.screen.get_width(), self.screen.get_height() * 0.025), score_counter,
                                (self.green_color[0], self.green_color[1]))

            pygame.display.update()

    def end_of_game(self):
        text = "You Lost..."
        x = self.screen.get_width() * 0.5
        y = self.screen.get_height() * 0.5

        self.draw_game_info((x, y), text, (self.red_color[0], self.red_color[1]))
        pygame.display.update()

        try:
            prior_highscore = utils.get_high_score()
        except FileNotFoundError:
            prior_highscore = 0
            utils.write_high_score(prior_highscore)

        if self.score > prior_highscore:
            utils.write_high_score(int(self.score))

            text = "New Highscore: " + str(utils.get_high_score())
            self.draw_game_info((x, y * 1.4), text, (self.red_color[0], self.red_color[1]))
            pygame.display.update()

        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False
