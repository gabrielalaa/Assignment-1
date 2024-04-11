class Issue(object):
    def __init__(self, issue_id: int, release_date: str, number_of_pages: int, released: bool = False, editor_id: int = None):
        self.issue_id = issue_id
        self.release_date = release_date
        self.number_of_pages = number_of_pages
        self.released: bool = released
        self.editor_id = editor_id

    def set_editor(self, editor_id: int):
        self.editor_id = editor_id

