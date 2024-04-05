from typing import List

from .newspaper import Newspaper


class Subscriber:
    def __init__(self, subscriber_id: int, name: str, address: str):
        self.id = subscriber_id
        self.name = name
        self.address = address
        # The list of newspapers that they are subscribed to
        self.subscriptions: List[Newspaper] = []

    def subscribe(self, newspaper: Newspaper):
        self.subscriptions.append(newspaper)

    def unsubscribe(self, newspaper: Newspaper):
        self.subscriptions = [sub for sub in self.subscriptions if sub.paper_id != newspaper.paper_id]

    def add(self):
        pass

    def remove(self):
        pass

    def update(self):
        pass

