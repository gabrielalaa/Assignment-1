from typing import List, Union, Optional

from .issue import Issue
from .newspaper import Newspaper


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []

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
    # TODO: check if paper_id: int and issue; error handling
    def add_issue_to_newspaper(self, paper_id: Union[int, str], issue: Issue):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            newspaper.issues.append(issue)
        else:
            # What if the newspaper does not exist?
            pass

    # example with error handling
    # def add_issue_to_newspaper(self, paper_id: Union[int, str], issue: Issue):
    #     newspaper = self.get_newspaper(paper_id)
    #     if newspaper is not None:
    #         if not any(i.issue_id == issue.issue_id for i in newspaper.issues):
    #             newspaper.issues.append(issue)
    #         else:
    #             # Handle the case where the issue ID already exists
    #             raise ValueError(f"Issue with ID {issue.issue_id} already exists in newspaper {paper_id}.")
    #     else:
    #         # Handle the case where the newspaper does not exist
    #         raise ValueError(f"Newspaper with ID {paper_id} does not exist.")

    # TODO: check if paper_id: int and issue; error handling
    def remove_issue_from_newspaper(self, paper_id: Union[int, str], issue_id: int):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is not None:
            newspaper.issues = [issue for issue in newspaper.issues if issue.issue_id != issue_id]
        else:
            pass

    # TODO: implement me
    def update_issue_in_newspaper(self, paper_id: Union[int, str], issue_id: int):
        pass
