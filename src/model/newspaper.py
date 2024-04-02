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

    # METHODS
    # Set default values of 'None'
    # If a value is not provided, do not update the attribute
    def update_newspaper(self, paper_id: int = None, frequency: int = None, price: float = None):
        if paper_id is not None:
            self.paper_id = paper_id
        if frequency is not None:
            self.frequency = frequency
        if price is not None:
            self.price = price

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    def remove_issue(self, issue_id):
        # Remove the issue based on its ID
        self.issues = [issue for issue in self.issues if issue.issue_id != issue_id]

    def update_issue(self, issue_id: int, issue_release_date=None, issue_pages: int = None, status: bool = None):
        # Find the issue by its ID
        for issue in self.issues:
            if issue.issue_id == issue_id:
                # Update it if new values are provided
                if issue_release_date is not None:
                    issue.release_date = issue_release_date
                if issue_pages is not None:
                    issue.number_of_pages = issue_pages
                if status is not None:
                    issue.released = status
                break  # No need to iterate anymore


# Adding/Removing Newspapers should be implemented here also?
# Maybe in another part of the project

# Model ? -> JSON

# error handling ? - what if an issue doesn't exists ?
