from typing import List

from .newspaper import Newspaper


class Subscriber:
    def __init__(self, subscriber_id: int, name: str, address: str):
        self.subscriber_id = subscriber_id
        self.subscriber_name = name
        self.subscriber_address = address
        # TODO: The list of newspapers that they are subscribed to
        self.subscriptions: List[Newspaper] = []

