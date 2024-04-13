from ..src.model.agency import Agency
from ..src.model.newspaper import Newspaper


def create_newspapers(agency: Agency):
    paper1 = Newspaper(paper_id=100, name="The New York Times", frequency=7, price=13.14)
    paper2 = Newspaper(paper_id=101, name="Heute", frequency=1, price=1.12)
    paper3 = Newspaper(paper_id=115, name="Wall Street Journal", frequency=1, price=3.00)
    paper4 = Newspaper(paper_id=125, name="National Geographic", frequency=30, price=34.00)
    agency.newspapers.extend([paper1, paper2, paper3, paper4])


# Populate the agency with data before tests are run
def populate(agency: Agency):
    create_newspapers(agency)
