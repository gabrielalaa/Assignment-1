from typing import List

from .newspaper import Newspaper
from .issue import Issue


class Subscriber:
    def __init__(self, subscriber_id: int, name: str, address: str):
        self.subscriber_id = subscriber_id
        self.subscriber_name = name
        self.subscriber_address = address
        self.subscriptions: List[int] = []
        self.delivered_issues: List[Issue] = []
