
class Issue(object):

    # I considered adding an ID because it is easy to be used for methods such as remove or update
    def __init__(self, issue_id: int, release_date, number_of_pages: int, released: bool = False):
        self.issue_id = issue_id
        self.release_date = release_date
        self.number_of_pages = number_of_pages
        self.released: bool = released
        self.editor = None

    def set_editor(self, editor):
        self.editor = editor


