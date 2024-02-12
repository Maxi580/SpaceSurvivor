import pygame


class Mothership:
    def __init__(self, screen_width, screen_height, surface):
        self.width = 0.5 * screen_width
        self.height = self.width
        self.x = screen_width * 0.5 - self.width * 0.5
        self.y = -self.height * 0.7
        self.picture = pygame.transform.scale(surface, (self.width, self.height))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
