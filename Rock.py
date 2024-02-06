class Rock:
    def __init__(self, x: int, width: int, height: int, size: int):
        self.width = size * (width / 8)
        self.height = size * (height / 8)
        self.x = x
        self.y = 0 - self.height

        self.size = size
        self.hp = 100 * size
        self.velocity = 5

    def update_rock_coordinates(self):
        self.y += self.velocity

    def below_screen(self, height) -> bool:
        if self.y > height:
            return True
        else:
            return False

    def adjust_size_to_window_resize(self, old_window_width: int, old_window_height: int,
                                     new_window_width: int, new_window_height: int):
        self.x = (self.x / old_window_width) * new_window_width
        self.y = (self.y / old_window_height) * new_window_height

        self.width = self.size * (new_window_width / 8)
        self.height = self.size * (new_window_height / 8)



