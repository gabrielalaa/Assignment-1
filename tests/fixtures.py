
import pytest

from ..src.app import create_app
from ..src.model.agency import Agency
from .testdata import populate


# Create the Flask application instance that I will be testing against
@pytest.fixture()
def app():
    yield create_app()


# Simulate requests without running the server
@pytest.fixture()
def client(app):
    yield app.test_client()


# Set up the Agency singleton instance and populate it with data before each test!
@pytest.fixture()
def agency(app):
    # This should reset the singleton and fix the first test which failed
    Agency.singleton_instance = None
    agency = Agency.get_instance()
    populate(agency)
    yield agency

