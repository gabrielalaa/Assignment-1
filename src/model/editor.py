from typing import List, Optional

from flask_restx import Model

from .newspaper import Newspaper
from .issue import Issue


class Editor(object):
    def __init__(self, editor_id: int, editor_name: str, address: str):
        self.editor_id = editor_id
        self.editor_name = editor_name
        self.address = address
        self.newspapers: List[Newspaper] = []
        self.issues: List[Issue] = []

