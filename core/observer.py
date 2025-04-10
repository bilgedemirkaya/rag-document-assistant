'''Observer Base Classes'''

class Observer:
    def update(self, event_type: str, data: dict):
        pass

class Observable:
    def __init__(self):
        self._observers = []

    def register(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)
