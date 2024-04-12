import parser

from flask import jsonify
# Import abort to handel errors
from flask_restx import Namespace, reqparse, Resource, fields, abort

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue

# Use a simple generator for ID's
import random

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
                               help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
                          help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
                                help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and '
                                     '7 for weekly magazines'),
    'price': fields.Float(required=True,
                          help='The monthly price of the newspaper (e.g. 12.3)')
})

issue_model = newspaper_ns.model('IssueModel', {
    'issue_id': fields.Integer(required=False,
                               help='The unique identifier of an issue'),
    'release_date': fields.String(required=True,
                                  help='The release date of the issue'),
    'number_of_pages': fields.Integer(required=True,
                                      help='The number of pages in the issue'),
    'released': fields.Boolean(required=False,
                               default=False,
                               help='The status of an issue'),
    'editor_id': fields.Integer(required=False,
                                help='The unique identifier of an editor')
})


@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        # Create a unique and simple ID
        paper_id = random.randint(1, 999)
        # Check if ID already exists
        while any(newspaper.paper_id == paper_id for newspaper in Agency.get_instance().newspapers):
            paper_id = random.randint(10, 99)

        # I was thinking to use uuid module in order to get real unique ID, but I think random is much better in such
        # a project when I care more about the functionality
        # paper_id = int(str(uuid.uuid4().int)[:8])

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):
    # Use 'reqparse' from flask_restx for parsing incoming request data
    # Define it
    parser = reqparse.RequestParser()
    # Add expected arguments
    parser.add_argument('name', type=str, required=False, help="Name of the newspaper")
    parser.add_argument('frequency', type=int, required=False, help="Frequency of the newspaper in days")
    parser.add_argument('price', type=float, required=False, help="Monthly price of the newspaper")

    @newspaper_ns.doc(description="Get a newspaper's information.")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        # Manage the situation when the newspaper is not found
        if search_result is None:
            # 404 is used for 'Not found'
            abort(404, message=f"No newspaper with ID {paper_id} found")
        return search_result

    @newspaper_ns.doc(description="Update a new newspaper")
    @newspaper_ns.expect(parser, validate=False)  # Expect fields from parser without strict validation
    # marshal_with may get a conflict with jsonify !!!
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            abort(404, message=f"No newspaper with ID {paper_id} found")

        # Create a flag to track if any update was made
        updated = False
        # Update the newspaper if arguments exist
        if arguments['name'] is not None:
            search_result.name = arguments['name']
            updated = True
        if arguments['frequency'] is not None:
            search_result.frequency = arguments['frequency']
            updated = True
        if arguments['price'] is not None:
            search_result.price = arguments['price']
            updated = True

        if not updated:
            abort(400, message=f"No updates have been made")

        return search_result

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")

    # TODO: get - stats


# Issues Endpoints
@newspaper_ns.route('/<int:paper_id>/issue')
class NewspaperIssues(Resource):
    @newspaper_ns.doc(description="List all issues of a specific newspaper")
    @newspaper_ns.marshal_with(issue_model, envelope="issue")
    def get(self, paper_id):
        search_result = Agency.get_instance().get_issues(paper_id)
        if search_result is None:
            abort(404, message=f"No newspaper with ID {paper_id} found")
        return search_result

    @newspaper_ns.doc(issue_model, description="Create a new issue")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope="issue")
    def post(self, paper_id):
        # Extract the issue data from payload
        issue_data = newspaper_ns.payload
        try:
            # Add the new issue, to the specified newspaper
            new_issue = Agency.get_instance().add_issue_to_newspaper(paper_id, issue_data)
            # Return the new issue
            return new_issue
        except ValueError:
            newspaper_ns.abort(404, message=f"No newspaper with ID {paper_id} found")


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class NewspaperIssueID(Resource):
    @newspaper_ns.doc(description="Get information of a newspaper issue")
    @newspaper_ns.marshal_with(issue_model, envelope="issue")
    def get(self, paper_id, issue_id):
        search_result = Agency.get_instance().get_issue(paper_id, issue_id)
        if search_result is None:
            abort(404, message=f"No issue with ID {issue_id} found")
        else:
            return search_result


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class NewspaperIssueRelease(Resource):
    @newspaper_ns.doc(description="Release an issue")
    # @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope="issue")
    def post(self, paper_id, issue_id):
        # This time I cannot check if the action is None, therefore try:
        try:
            release_action = Agency.get_instance().release_issue(paper_id, issue_id)
            return release_action
        except ValueError as err:
            # Since the error can be due to various reasons, try to handle all situations:
            message = str(err)
            # The newspaper doesn't exist
            if "newspaper" in message:
                abort(404, message=message)
            # The issue doesn't exist
            elif "doesn't exist" in message:
                abort(404, message=message)
            else:
                # The issue has already been released
                abort(400, message=message)


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class NewspaperIssueEditor(Resource):
    # Use reqparse because I only need one argument
    parser = reqparse.RequestParser()
    parser.add_argument('editor_id', type=int, required=True, help='The unique identifier of an editor')

    @newspaper_ns.doc(description="Specify an editor for an issue")
    @newspaper_ns.expect(parser, validate=False)  # Expect fields from parser without strict validation
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id, issue_id):
        # Get and set the editor_id
        arguments = self.parser.parse_args()
        editor_id = arguments['editor_id']

        try:
            update_issue = Agency.get_instance().specify_editor(paper_id, issue_id, editor_id)
            return update_issue
        except ValueError as err:
            # Since the error can be due to various reasons, try to handle all situations:
            message = str(err)
            # The newspaper doesn't exist
            if "newspaper" in message:
                abort(404, message=message)
            # The issue doesn't exist
            elif "issue" in message:
                abort(404, message=message)
            else:
                # The editor doesn't exist
                abort(404, message=message)


# TODO:
@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/deliver')
class NewspaperIssueDeliver(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('subscriber_id', type=int, required=True, help='The unique identifier of a subscriber')

    @newspaper_ns.doc(description="Send an issue to a subscriber")
    @newspaper_ns.expect(parser, validate=False) # Expect fields from parser without strict validation
    # @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id, issue_id):
        # Get and set the subscriber_id
        arguments = self.parser.parse_args()
        subscriber_id = arguments['subscriber_id']
        pass



