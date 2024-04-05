from typing import List

from flask_restx import Model

from .newspaper import Newspaper
from .issue import Issue


class Editor(object):
    def __init__(self, editor_id: int, editor_name: str, address: str):
        self.editor_id = editor_id
        self.editor_name = editor_name
        self.address = address
        self.newspaper: List[Newspaper] = []
        # Create a dictionary with newspapers and issues
        # self.newspaper_issues: Dict[Newspaper, Issue] =


# Create another class to handle the editors and their methods
class System:
    def __init__(self):
        # Store instances of 'Editor' in the system
        self.editors: List[Editor] = []

    # METHODS
    def add_editor(self, editor: Editor):
        self.editors.append(editor)

    # Remove editor and transfer all issues to another editor of the same newspaper
    def remove_editor(self, editor_id: int):
        editor_to_remove = None
        for editor in self.editors:
            if editor.editor_id == editor_id:
                # Find the editor based on ID
                editor_to_remove = editor
                break

        # If the editor is found
        if editor_to_remove:
            # Try to find another editor with the same newspapers
            for newspaper in editor_to_remove.newspaper:
                new_editor = self.find_editor(newspaper.paper_id, editor_id)
                if new_editor:
                    # Transfer issues
                    for issue in newspaper.issues:
                        issue.editor_id = new_editor.editor_id

            # Remove the editor
            self.editors.remove(editor_to_remove)

    def find_editor(self, newspaper_id: int, remove_editor_id: int) -> Editor:
        for editor in self.editors:
            if newspaper_id in editor.newspaper and editor.editor_id != remove_editor_id:
                return editor

    def update_editor(self, editor_id: int, name: str = None, address: str = None, newspaper: List[Newspaper] = None):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                # Update it if new values are provided
                if name is not None:
                    editor.name = name
                if address is not None:
                    editor.address = address
                if newspaper is not None:
                    editor.newspaper = newspaper
                break  # No need to iterate anymore
