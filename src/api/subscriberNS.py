from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort

from ..model.agency import Agency
from ..model.subscriber import Subscriber

# Use a simple generator for ID's
import random

subscriber_ns = Namespace("subscriber", description="Subscriber related operations")

subscriber_model = subscriber_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
                                    help='The unique identifier of a subscriber'),
    'subscriber_name': fields.String(required=True,
                                     help='The name of the subscriber'),
    'subscriber_address': fields.String(required=True,
                                        help='this is the address of the subscriber')
})


@subscriber_ns.route('/')
class SubscriberAPI(Resource):

    @subscriber_ns.doc(subscriber_model, description="Add a new subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        # Create a unique and simple ID
        subscriber_id = random.randint(100000, 999999)
        # Check if ID already exists
        while any(subscriber.subscriber_id == subscriber_id for subscriber in Agency.get_instance().subscribers):
            subscriber_id = random.randint(100000, 999999)

        # create a new subscriber object and add it
        new_subscriber = Subscriber(subscriber_id=subscriber_id,
                                    name=subscriber_ns.payload['name'],
                                    address=subscriber_ns.payload['address'])
        Agency.get_instance().add_subscriber(new_subscriber)

        # return the new subscriber
        return new_subscriber

    @subscriber_ns.marshal_list_with(subscriber_model, envelope='subscriber')
    def get(self):
        return Agency.get_instance().all_subscriber()


@subscriber_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('subscriber_name', type=str, required=False, help="The name of the subscriber")
    parser.add_argument('subscriber_address', type=str, required=False, help="The address of the subscriber")

    @subscriber_ns.doc(description="Get a new subscriber")
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def get(self, subscriber_id):
        search_result = Agency.get_instance().get_subscriber(subscriber_id)
        # Manage the situation when the subscriber is not found
        if search_result is None:
            # 404 is used for 'Not found'
            abort(404, message=f"No subscriber with ID {subscriber_id} found")
        return search_result

    @subscriber_ns.doc(description="Update a new subscriber")
    @subscriber_ns.expect(parser, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_subscriber(subscriber_id)
        if not search_result:
            abort(404, message=f"No subscriber with the ID {subscriber_id} was found")

        updated = False
        if arguments['subscriber_name'] is not None:
            search_result.name = arguments['subscriber_name']
            updated = True
        if arguments['subscriber_address'] is not None:
            search_result.address = arguments['subscriber_address']
            updated = True

        if not updated:
            abort(404, message=f"No updates have been made")

        return search_result

    @subscriber_ns.doc(description="Delete a new subscriber")
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        Agency.get_instance().remove_subscriber(targeted_subscriber)
        return jsonify(f"Subscriber with ID {subscriber_id} was removed")
