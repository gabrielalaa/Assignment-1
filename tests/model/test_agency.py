import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.issue import Issue
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
from ..fixtures import app, client, agency


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

