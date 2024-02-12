from abc import abstractmethod
from msilib.schema import Property


class Entity:
    @abstractmethod
    def __init__(self):
        self.xy = "one"

    @abstractmethod
    def update_coordinates(self, *args, **kwargs):
        pass

