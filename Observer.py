class Observer:
    def update(self, event):
        pass


class ResizeObserver(Observer):
    def __init__(self, entity, screen_width: int, screen_height: int):
        self.entity = entity
        self.current_screen_width = screen_width
        self.current_screen_height = screen_height

    def update(self, event):
        self.entity.update_size(event.w, event.h, self.current_screen_width, self.current_screen_height)
        self.current_screen_width = event.w
        self.current_screen_height = event.h


class WindowResizeSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

