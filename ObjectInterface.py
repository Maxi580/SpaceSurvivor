from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def __init__(self):
        self.xy = "one"

    @abstractmethod
    def update_coordinates(self, *args, **kwargs):
        pass

