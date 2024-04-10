from typing import List, Union, Optional

from .issue import Issue
from .newspaper import Newspaper
from .subscriber import Subscriber
from .editor import Editor


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
        # Assert that ID does not exist  yet (or create a new one)
        if any(new_paper.paper_id == paper.paper_id for paper in self.newspapers):
            raise ValueError(f'A newspaper with ID {new_paper.paper_id} already exists!')
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

    def add_issue_to_newspaper(self, paper_id: int, issue: Issue):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            newspaper.issues.append(issue)
        else:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

    def release_issue(self, paper_id: int, issue_id: int):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            issue = self.get_issue(paper_id, issue_id)
            if issue is not None:
                issue.released = True
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

    #    def add_editor(self, new_editor: Editor):
    #         # TODO: assert that ID does not exist  yet (or create a new one)
    #         self.editors.append(new_editor)
    #
    #     def get_editor(self, editor_id: Union[int, str]) -> Optional[Editor]:
    #         for editor in self.editors:
    #             if editor.editor_id == editor_id:
    #                 return editor
    #         return None
    #
    #     def all_editor(self) -> List[Editor]:
    #         return self.editors
    #
    #     def remove_editor(self, editor: Editor):
    #         self.editors.remove(editor)
    #
    #     def editor_issues(self , editor_id: Union[int, str]) -> list[Issue] | None:
    #         for editor in self.editors:
    #             if editor.editor_id == editor_id:
    #                 return editor.issues
    #         return None
    #     def add_subscriber(self, new_subscriber: Subscriber):
    #         # TODO: assert that ID does not exist  yet (or create a new one)
    #         self.subscribers.append(new_subscriber)
    #
    #     def get_subscriber(self, subscriber_id: Union[int, str]) -> Optional[Subscriber]:
    #         for subscriber in self.subscribers:
    #             if subscriber.subscriber_id == subscriber_id:
    #                 return subscriber
    #         return None
    #
    #     def all_subscriber(self) -> List[Subscriber]:
    #         return self.subscribers
    #
    #     def remove_subscriber(self, subscriber: Subscriber):
    #         self.subscribers.remove(subscriber)
