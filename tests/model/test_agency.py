import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.issue import Issue
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
from ..fixtures import app, client, agency


# Tests for newspaper
def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


def test_add_newspaper_same_id_should_raise_error(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                           name="Superman Comic",
                           frequency=7,
                           price=13.14)

    with pytest.raises(ValueError,
                       match='A newspaper with ID 999 already exists!'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)


def test_get_newspaper(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)

    paper = agency.get_newspaper(new_paper.paper_id)
    assert paper == new_paper
    assert paper.name == "Simpsons Comic"
    assert paper.frequency == 7
    assert paper.price == 3.14


def test_get_newspaper_as_none(agency):
    paper = agency.get_newspaper(1000)
    assert paper is None


def test_all_newspapers(agency):
    before = len(agency.newspapers)
    # Add some newspapers
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    new_paper2 = Newspaper(paper_id=500,
                           name="Daily Pulse",
                           frequency=4,
                           price=10)
    agency.add_newspaper(new_paper2)

    papers = agency.all_newspapers()

    # Check if new papers are added
    assert len(papers) == before + 2


def test_remove_newspaper(agency):
    # Save the length
    before = len(agency.newspapers)
    # Add a newspaper
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)

    # Add an editor
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    # Increase the list of editors the agency has in the constructor
    agency.editors.append(new_editor)
    # Add the newspaper in editor's list
    new_editor.newspapers.append(new_paper)

    # Add a subscriber
    new_subscriber = Subscriber(subscriber_id=100001,
                                name="Gabriela",
                                address="San Francisco")
    # Increase the list of subscribers the agency has in the constructor
    agency.subscribers.append(new_subscriber)
    # Add the newspaper ID in subscriber's list
    new_subscriber.subscriptions.append(new_paper.paper_id)

    # Add an issue
    # Make sure to be released and to have the id of the editor
    new_issue = Issue(issue_id=1000,
                      release_date="14.04.2024",
                      number_of_pages=10,
                      released=True,
                      editor_id=new_editor.editor_id)
    # Specify the editor and deliver the issue
    new_paper.issues.append(new_issue)
    new_editor.issues.append(new_issue)
    new_subscriber.delivered_issues.append(new_issue)

    # After removing the newspaper the current length remains the same as before
    agency.remove_newspaper(new_paper)
    assert len(agency.newspapers) == before

    # Check if the newspaper is removed from agency, editor and subscriber
    assert new_paper not in agency.newspapers
    assert new_paper not in new_editor.newspapers
    assert new_paper.paper_id not in new_subscriber.subscriptions

    # Check if the issue is removed
    assert new_issue not in new_editor.issues
    assert new_issue not in new_subscriber.delivered_issues

    # Check if the paper list is cleared
    assert len(new_paper.issues) == 0


def test_get_newspaper_stats(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    # Create subscribers
    new_subscriber = Subscriber(subscriber_id=100001,
                                name="Gabriela",
                                address="San Francisco")
    # Subscribe them to the newspaper
    new_subscriber.subscriptions.append(new_paper.paper_id)
    # Increase the list of subscribers the agency has in the constructor
    agency.subscribers.append(new_subscriber)
    new_subscriber2 = Subscriber(subscriber_id=100002,
                                 name="Carla",
                                 address="San Francisco")
    new_subscriber2.subscriptions.append(new_paper.paper_id)
    agency.subscribers.append(new_subscriber2)

    statistics = agency.get_newspaper_stats(new_paper.paper_id)

    assert statistics["number_of_subscribers"] == 2
    assert statistics["monthly_revenue"] == 2
    assert statistics["annual_revenue"] == 24


# Tests for issues
def test_get_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    new_issue = agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)

    issue = agency.get_issue(new_paper.paper_id, new_issue.issue_id)
    assert issue == new_issue
    assert issue.release_date == "14.04.2024"


def test_get_issue_as_none(agency):
    fake_paper_id = 1000
    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    issue = agency.get_issue(fake_paper_id, issue_data)
    assert issue is None


def test_get_issues(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)

    issue_data2 = {"release_date": "14.04.2024",
                   "number_of_pages": 10}
    agency.add_issue_to_newspaper(new_paper.paper_id, issue_data2)

    issues = agency.get_issues(new_paper.paper_id)

    assert len(issues) == 2
    assert issues[0].release_date == "14.04.2024"
    assert issues[1].number_of_pages == 10


def test_add_issue_to_newspaper(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    new_issue = agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)

    paper = agency.get_newspaper(new_paper.paper_id)
    assert new_issue in paper.issues
    assert new_issue.release_date == "14.04.2024"
    assert new_issue.number_of_pages == 10
    # Check if it remains false as default
    assert not new_issue.released


def test_test_add_issue_to_nonexistent_newspaper_should_raise_error(agency):
    fake_paper_id = 1000
    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    with pytest.raises(ValueError,
                       match=f"A newspaper with ID {fake_paper_id} doesn't exist!"):
        agency.add_issue_to_newspaper(fake_paper_id, issue_data)


# Release issue with error handling
def test_release_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)
    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    issue = agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)

    # Success case
    released_issue = agency.release_issue(new_paper.paper_id, issue.issue_id)
    assert released_issue.released

    # Handle errors
    with pytest.raises(ValueError,
                       match=f"A newspaper with ID 99999 does not exist!"):
        agency.release_issue(99999, issue.issue_id)

    with pytest.raises(ValueError,
                       match=f"An issue with ID 1 doesn't exist!"):
        agency.release_issue(new_paper.paper_id, 1)

    with pytest.raises(ValueError,
                       match=f"An issue with ID {issue.issue_id} has already been released!"):
        agency.release_issue(new_paper.paper_id, issue.issue_id)


# Specify the editor with error handling
def test_specify_editor(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)
    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    new_issue = agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    # Increase the list of editors the agency has in the constructor
    agency.editors.append(new_editor)

    # Success case
    issue = agency.specify_editor(new_paper.paper_id, new_issue.issue_id, new_editor.editor_id)
    assert issue.editor_id == new_editor.editor_id

    # Handle errors
    with pytest.raises(ValueError,
                       match="A newspaper with ID 99999 doesn't exist!"):
        agency.specify_editor(99999, new_issue.issue_id, new_editor.editor_id)

    with pytest.raises(ValueError,
                       match="An issue with ID 1 doesn't exist!"):
        agency.specify_editor(new_paper.paper_id, 1, new_editor.editor_id)

    with pytest.raises(ValueError,
                       match="An editor with ID 2 doesn't exist!"):
        agency.specify_editor(new_paper.paper_id, new_issue.issue_id, 2)


def test_deliver_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)
    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    new_issue = agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)
    # Add a subscriber

    # Release the issue first
    new_issue.released = True

    new_subscriber = Subscriber(subscriber_id=100001,
                                name="Gabriela",
                                address="San Francisco")
    # Increase the list of subscribers the agency has in the constructor
    agency.subscribers.append(new_subscriber)

    # Success case:
    issue = agency.deliver_issue(new_paper.paper_id, new_issue.issue_id, new_subscriber.subscriber_id)
    assert issue in new_subscriber.delivered_issues

    # Handle errors
    with pytest.raises(ValueError,
                       match="A newspaper with ID 99999 doesn't exist!"):
        agency.deliver_issue(99999, new_issue.issue_id, new_subscriber.subscriber_id)

    with pytest.raises(ValueError,
                       match="An issue with ID 1 doesn't exist!"):
        agency.deliver_issue(new_paper.paper_id, 1, new_subscriber.subscriber_id)

    with pytest.raises(ValueError,
                       match="A subscriber with ID 2 doesn't exist!"):
        agency.deliver_issue(new_paper.paper_id, new_issue.issue_id, 2)


def test_deliver_unreleased_issue(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)
    issue_data = {"release_date": "14.04.2024",
                  "number_of_pages": 10}
    new_issue = agency.add_issue_to_newspaper(new_paper.paper_id, issue_data)
    # Do not release the issue

    # Add a subscriber
    new_subscriber = Subscriber(subscriber_id=100001,
                                name="Gabriela",
                                address="San Francisco")
    # Increase the list of subscribers the agency has in the constructor
    agency.subscribers.append(new_subscriber)

    with pytest.raises(ValueError,
                       match=f"Issue with ID {new_issue.issue_id} has not been released yet!"):
        agency.deliver_issue(new_paper.paper_id, new_issue.issue_id, new_subscriber.subscriber_id)


# Tests for newspaper
def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)
    assert len(agency.all_editor()) == before + 1


def test_add_editor_same_id_should_raise_error(agency):
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    # first adding of newspaper should be okay
    agency.add_editor(new_editor)

    new_editor2 = Editor(editor_id=10000,
                         editor_name="Ana",
                         address="San Francisco")
    with pytest.raises(ValueError,
                       match="An editor with ID 10000 already exists!"):
        agency.add_editor(new_editor2)


def test_get_editor(agency):
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)

    editor = agency.get_editor(new_editor.editor_id)
    assert editor == new_editor
    assert editor.editor_name == "Ana"
    assert editor.address == "San Francisco"


def test_get_editor_as_none(agency):
    editor = agency.get_editor(1)
    assert editor is None


def test_all_editor(agency):
    before = len(agency.editors)
    # Add some editors
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)
    new_editor2 = Editor(editor_id=10001,
                         editor_name="Ana",
                         address="San Francisco")
    agency.add_editor(new_editor2)

    editors = agency.all_editor()

    assert len(editors) == before + 2


def test_remove_editor(agency):
    # Save the length
    before = len(agency.editors)
    # Add an editor
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)

    agency.remove_editor(new_editor)
    # After removing the editor the current length remains the same as before
    assert len(agency.editors) == before
    assert new_editor not in agency.editors


# Add newspaper to editor with error handling
def test_add_newspaper_to_editor(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)

    agency.add_newspaper_to_editor(new_paper.paper_id, new_editor.editor_id)
    # Success case
    assert new_paper in new_editor.newspapers

    # Handle errors
    with pytest.raises(ValueError,
                       match="A newspaper with ID 1000 doesn't exist!"):
        agency.add_newspaper_to_editor(1000, new_editor.editor_id)

    with pytest.raises(ValueError,
                       match="An editor with ID 1 doesn't exist!"):
        agency.add_newspaper_to_editor(new_paper.paper_id, 1)


def test_transfer_issues(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)
    new_editor2 = Editor(editor_id=10001,
                         editor_name="Ana",
                         address="San Francisco")
    agency.add_editor(new_editor2)

    new_issue = Issue(issue_id=1000,
                      release_date="14.04.2024",
                      number_of_pages=10,
                      released=False,
                      editor_id=new_editor.editor_id)
    new_paper.issues.append(new_issue)

    # Assign the newspaper and the issue to the first editor
    new_editor.newspapers.append(new_paper)
    new_editor.issues.append(new_issue)

    # Assign the newspaper to the second one, simulate his existence
    new_editor2.newspapers.append(new_paper)

    # After removing the first editor, the second one should receive the issue because the newspaper was assigned to him
    agency.transfer_issues(new_editor)
    assert new_issue in new_editor2.issues


def test_transfer_issues_no_other_editor(agency):
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=1)
    agency.add_newspaper(new_paper)

    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)

    new_issue = Issue(issue_id=1000,
                      release_date="14.04.2024",
                      number_of_pages=10,
                      released=True,
                      editor_id=new_editor.editor_id)
    new_paper.issues.append(new_issue)

    new_editor.newspapers.append(new_paper)
    new_editor.issues.append(new_issue)

    # When removing the editor from the system and there is no other editor assigned to the same newspaper,
    # the issue is no longer assigned to someone else
    agency.transfer_issues(new_editor)
    assert new_issue.editor_id is None


def test_editor_issues(agency):
    new_editor = Editor(editor_id=10000,
                        editor_name="Ana",
                        address="San Francisco")
    agency.add_editor(new_editor)

    new_issue = Issue(issue_id=1000,
                      release_date="14.04.2024",
                      number_of_pages=10,
                      released=False,
                      editor_id=new_editor.editor_id)
    new_editor.issues.append(new_issue)
    issues = agency.editor_issues(new_editor.editor_id)
    assert issues == [new_issue]
    assert new_issue in issues


def test_editor_issues_no_editor_found(agency):
    issues = agency.editor_issues(2000)
    assert issues is None

