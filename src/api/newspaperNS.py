from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper

# import random

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


@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        # TODO: this is not smart! you should find a better way to generate a unique ID!
        # paper_id = random.randint(10, 99)
        # OPTIONAL CHECK if ID already exists
        # while any(newspaper.paper_id == paper_id for newspaper in Agency.get_instance().newspapers):
        #   paper_id = random.randint(10, 99)
        paper_id = len(Agency.get_instance().newspapers) + 20

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

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    # Use 'reqparse' from flask_restx for parsing incoming request data
    # Define it
    parser = reqparse.RequestParser()
    # Add expected arguments
    parser.add_argument('name', type=str, required=False, help="Name of the newspaper")
    parser.add_argument('frequency', type=int, required=False, help="Frequency of the newspaper in days")
    parser.add_argument('price', type=int, required=False, help="Monthly price of the newspaper")

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            return f'No newspaper found with ID {paper_id}'

        # Update the newspaper if arguments exist
        if arguments['name'] is not None:
            search_result.name = arguments['name']
        if arguments['frequency'] is not None:
            search_result.frequency = arguments['frequency']
        if arguments['price'] is not None:
            search_result.price = arguments['price']

        return search_result

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
