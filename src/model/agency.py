from typing import List, Union, Optional

from . import subscriber
from .issue import Issue
from .newspaper import Newspaper
from .subscriber import Subscriber
from .editor import Editor

import random
import datetime


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.subscribers: List[Subscriber] = []
        self.editors: List[Editor] = []

    # This ensures that only one instance of 'Agency' exists (Singleton pattern)
    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        # Assert that ID does not exist
        if any(new_paper.paper_id == paper.paper_id for paper in self.newspapers):
            raise ValueError(f"A newspaper with ID {new_paper.paper_id} already exists!")
        self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int, str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)

    # METHODS for issues
    def get_issue(self, paper_id: int, issue_id: int) -> Optional[Issue]:
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            for issue in newspaper.issues:
                if issue.issue_id == issue_id:
                    return issue
            return None

    def get_issues(self, paper_id: int) -> Optional[List[Issue]]:
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            return newspaper.issues
        else:
            return None

    def generate_unique_issue_id(self, newspaper):
        new_issue_id = random.randint(1000, 9999)
        while any(issue.issue_id == new_issue_id for issue in newspaper.issues):
            new_issue_id = random.randint(100, 199)
        return new_issue_id

    def add_issue_to_newspaper(self, paper_id: int, issue_data):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        # Remove issue_id from the data to avoid conflict !!!
        issue_data.pop("issue_id", None)

        # Generate a unique ID for the issue
        unique_issue_id = self.generate_unique_issue_id(newspaper)

        # Specify the status of the issue and the release date
        issue_data.setdefault("released", False)
        issue_data.setdefault("release_date", None)

        # Create a new Issue object using the ID
        new_issue = Issue(issue_id=unique_issue_id, **issue_data)

        # Add the issue to the newspaper
        newspaper.issues.append(new_issue)
        return new_issue

    def release_issue(self, paper_id: int, issue_id: int):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            issue = self.get_issue(paper_id, issue_id)
            # Check if the issue exists and if it was not yet been released
            if issue is not None and not issue.released:
                issue.released = True
                # If I release an issue, set the current datetime in a format of YYYY-MM-DD
                issue.release_date = datetime.datetime.now().strftime("%Y-%m-%d")
                return issue
            elif issue.released:
                raise ValueError(f"An issue with ID {issue_id} has already been released!")
            else:
                raise ValueError(f"An issue with ID {issue_id} doesn't exist!")
        else:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

    def specify_editor(self):
        pass

    # # TODO: check if paper_id: int and issue; error handling
    # def remove_issue_from_newspaper(self, paper_id: Union[int, str], issue_id: int):
    #     newspaper = self.get_newspaper(paper_id)
    #     if newspaper is not None:
    #         newspaper.issues = [issue for issue in newspaper.issues if issue.issue_id != issue_id]
    #     else:
    #         pass
    #
    # # TODO: implement me
    # def update_issue_in_newspaper(self, paper_id: Union[int, str], issue_id: int):
    #     pass

    # METHODS for editor
    def add_editor(self, new_editor: Editor):
        # Assert that ID does not exist  yet
        if any(new_editor.editor_id == editor.editor_id for editor in self.editors):
            raise ValueError(f"An editor with ID {new_editor.editor_id} already exists!")
        self.editors.append(new_editor)

    def get_editor(self, editor_id: Union[int, str]) -> Optional[Editor]:
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None

    def all_editor(self) -> List[Editor]:
        return self.editors

    def remove_editor(self, editor: Editor):
        self.editors.remove(editor)

    #  TODO:
    #     def editor_issues(self , editor_id: Union[int, str]) -> list[Issue] | None:
    #         for editor in self.editors:
    #             if editor.editor_id == editor_id:
    #                 return editor.issues
    #         return None

    # METHODS for subscriber
    def add_subscriber(self, new_subscriber: Subscriber):
        # Assert that ID does not exist  yet
        if any(new_subscriber.subscriber_id == sub.subscriber_id for sub in self.subscribers):
            raise ValueError(f"A subscriber with ID {new_subscriber.subscriber_id} already exists!")
        self.subscribers.append(new_subscriber)

    def get_subscriber(self, subscriber_id: Union[int, str]) -> Optional[Subscriber]:
        for sub in self.subscribers:
            if sub.subscriber_id == subscriber_id:
                return sub
        return None

    def all_subscribers(self) -> List[Subscriber]:
        return self.subscribers

    def remove_subscriber(self, sub: Subscriber):
        self.subscribers.remove(sub)
