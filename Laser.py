class Laser:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x + width * 0.4
        self.y = y
        self.height = height * 0.5
        self.width = width * 0.2

        self.velocity = 14

    def update_laser_coordinates(self):
        self.y -= self.velocity

    def outside_screen(self) -> bool:
        if self.y + self.height < 0:
            return True
        else:
            return False

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int,
                                     new_ship_width: int, new_ship_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = new_ship_width * 0.5
        self.height = new_ship_height * 0.2

