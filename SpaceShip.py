from pygame import Surface

from Laser import Laser


class SpaceShip:
    def __init__(self, width: int, height: int):
        self.x = width * 0.5
        self.y = height * 0.8
        self.width = width * 0.1
        self.height = height * 0.1

        self.velocity = 7
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.hp = 100

    def update_space_ship_coordinates(self, screen_width: int, screen_height: int):
        if self.moving_left:
            new_x_coordinate = self.x - self.velocity
            if new_x_coordinate > 0:
                self.x = new_x_coordinate
            else:
                self.x = 0
        if self.moving_right:
            new_x_coordinate = self.x + self.velocity
            x_maximum = (screen_width - self.width)
            if new_x_coordinate < x_maximum:
                self.x = new_x_coordinate
            else:
                self.x = x_maximum
        if self.moving_up:
            new_y_coordinate = self.y - self.velocity
            if new_y_coordinate > 0:
                self.y = new_y_coordinate
            else:
                self.y = 0
        if self.moving_down:
            new_y_coordinate = self.y + self.velocity
            y_minimum = (screen_height - self.height)
            if new_y_coordinate < y_minimum:
                self.y = new_y_coordinate
            else:
                self.y = y_minimum

    def take_hit(self):
        self.hp -= 25

    def shoot(self):
        return Laser(self.x, self.y, self.width, self.height)

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = new_window_width * 0.1
        self.height = new_window_height * 0.1


