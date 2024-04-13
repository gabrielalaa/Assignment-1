from typing import List, Union, Optional

from . import subscriber
from .issue import Issue
from .newspaper import Newspaper
from .subscriber import Subscriber
from .editor import Editor

import random


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

    def get_newspaper_stats(self, paper_id):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        # Count subscribers
        sub_count = sum(1 for sub in self.subscribers if paper_id in sub.subscriptions)

        # Calculate revenues
        monthly_revenue = sub_count * newspaper.price
        annual_revenue = monthly_revenue * 12

        return {
            "number_of_subscribers": sub_count,
            "monthly_revenue": monthly_revenue,
            'annual_revenue': annual_revenue
        }

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
            new_issue_id = random.randint(1000, 9999)
        return new_issue_id

    def add_issue_to_newspaper(self, paper_id: int, issue_data):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        # Remove issue_id from the data to avoid conflict !!!
        issue_data.pop("issue_id", None)
        # Exclude editor_id when creating a new issue!
        issue_data.pop("editor_id", None)

        # Generate a unique ID for the issue
        unique_issue_id = self.generate_unique_issue_id(newspaper)

        # Specify the status of the issue
        issue_data.setdefault("released", False)

        # Create a new Issue object using the ID
        new_issue = Issue(issue_id=unique_issue_id, **issue_data)

        # Add the issue to the newspaper
        newspaper.issues.append(new_issue)
        return new_issue

    def release_issue(self, paper_id: int, issue_id: int):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} does not exist!")

        issue = self.get_issue(paper_id, issue_id)
        # Check if the issue exists
        if issue is None:
            raise ValueError(f"An issue with ID {issue_id} doesn't exist!")

        # Check if the issue has been released
        if issue.released:
            raise ValueError(f"An issue with ID {issue_id} has already been released!")

        # Release it
        issue.released = True
        return issue

    def specify_editor(self, paper_id, issue_id, editor_id):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        # This also handle the situation in which I cannot specify an editor to an issue of another editor! (and
        # vice versa) - But the error message is a bit unclear now
        issue = self.get_issue(paper_id, issue_id)
        if issue is None:
            raise ValueError(f"A issue with ID {issue_id} doesn't exist!")

        editor = self.get_editor(editor_id)
        if editor is None:
            raise ValueError(f"An editor with ID {editor_id} doesn't exist!")

        # From my point of view, re-assignment should be possible
        # Set the editor
        issue.set_editor(editor_id)
        # Add the issue
        if issue not in editor.issues:
            editor.issues.append(issue)

        # Ensure the newspaper is assigned to the editor if not already
        if newspaper not in editor.newspapers:
            editor.newspapers.append(newspaper)

        return issue

    def deliver_issue(self, paper_id: int, issue_id: int, subscriber_id: int):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        issue = self.get_issue(paper_id, issue_id)
        if issue is None:
            raise ValueError(f"A issue with ID {issue_id} doesn't exist!")

        sub = self.get_subscriber(subscriber_id)
        if sub is None:
            raise ValueError(f"A subscriber with ID {subscriber_id} doesn't exist!")

        if newspaper not in sub.subscriptions:
            raise ValueError(f"Subscriber with ID {subscriber_id} is not subscribed to newspaper ID {paper_id}!")

        if not issue.released:
            raise ValueError(f"Issue with ID {issue_id} has not been released yet!")

        # Record the delivery in a list
        sub.delivered_issues.append(issue)

        return issue

    # # TODO: ?
    # def remove_issue_from_newspaper(self, paper_id: Union[int, str], issue_id: int):
    #     newspaper = self.get_newspaper(paper_id)
    #     if newspaper is not None:
    #         newspaper.issues = [issue for issue in newspaper.issues if issue.issue_id != issue_id]
    #     else:
    #         pass
    #
    # # TODO: ?
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

    # An editor may be responsible for the content of the newspaper, not just the issue
    def add_newspaper_to_editor(self, paper_id: int, editor_id: int):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        editor = self.get_editor(editor_id)
        if editor is None:
            raise ValueError(f"An editor with ID {editor_id} doesn't exist!")

        if newspaper not in editor.newspapers:
            editor.newspapers.append(newspaper)

    # When an editor is removed, transfer all issues to another editor of the same newspaper
    def transfer_issues(self, targeted_editor: Editor):
        # For each newspaper the editor has
        for paper in targeted_editor.newspapers:
            # Create a list of issues to be transferred
            issue_to_transfer = [issue for issue in paper.issues if issue.editor_id == targeted_editor.editor_id]

            # Find another editor and transfer issues
            for issue in issue_to_transfer:
                # Use a flag to check if the transfer take place
                transfer = False
                for editor in self.editors:
                    # Find another editor with the same newspaper assigned
                    if editor.editor_id != targeted_editor.editor_id and paper in editor.newspapers:
                        # Because I set only one editor to each issue, I assume that each issue has only one editor
                        # assigned
                        editor.issues.append(issue)
                        issue.set_editor(editor.editor_id)
                        transfer = True
                        break  # No need to iterate anymore
                if not transfer:
                    # Be sure that the issue doesn't remain set to this editor
                    issue.editor_id = None

    def editor_issues(self, editor_id: int) -> Optional[List[Issue]]:
        editor = self.get_editor(editor_id)
        if editor is not None:
            return editor.issues
        else:
            return None

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

    def subscribe(self, paper_id, subscriber_id):
        newspaper = self.get_newspaper(paper_id)
        if newspaper is None:
            raise ValueError(f"A newspaper with ID {paper_id} doesn't exist!")

        sub = self.get_subscriber(subscriber_id)
        if sub is None:
            raise ValueError(f"A subscriber with ID {subscriber_id} doesn't exist!")

        if paper_id in sub.subscriptions:
            return {"subscriptions": sub.subscriptions, "status": "Subscriber already subscribed to this paper!"}
        else:
            sub.subscriptions.append(paper_id)
            return {"subscriptions": sub.subscriptions, "status": "Subscriber successfully subscribed to this paper!"}

    def get_subscriber_stats(self, subscriber_id):
        sub = self.get_subscriber(subscriber_id)
        if sub is None:
            raise ValueError(f"A subscriber with ID {subscriber_id} doesn't exist!")

        # Extra details
        total_monthly_cost = 0
        total_annual_cost = 0
        details = []

        for paper_id in sub.subscriptions:
            newspaper = self.get_newspaper(paper_id)
            if newspaper:
                monthly_cost = newspaper.price
                annual_cost = monthly_cost * 12
                # Use a set for efficiency in checking
                issue_ids = {issue.issue_id for issue in newspaper.issues}
                number_of_issues = len([issue for issue in sub.delivered_issues if issue.issue_id in issue_ids])

                details.append({
                    "newspaper_id": paper_id,
                    "newspaper_name": newspaper.name,
                    "monthly_cost": monthly_cost,
                    "annual_cost": annual_cost,
                    "number_of_issues": number_of_issues
                })

                total_monthly_cost += monthly_cost
                total_annual_cost += annual_cost

        return {
            "number_of_subscriptions": len(sub.subscriptions),
            "total_monthly_cost": total_monthly_cost,
            "total_annual_cost": total_annual_cost,
            "details": details
        }
