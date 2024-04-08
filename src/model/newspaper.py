from typing import List

from flask_restx import Model

from .issue import Issue


class Newspaper(object):

    # CONSTRUCTOR
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        # This is expected to take a list of Issues as an argument.
        # Each element is an instance of the 'Issue' class.
        self.issues: List[Issue] = []

# TODO: Model ? -> JSON
