from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort

from ..model.agency import Agency
from ..model.editor import Editor

# Use a simple generator for ID's
import random

editor_ns = Namespace("editor", description="Editor related operations")

editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=False,
                                help='The unique identifier of an editor'),
    'editor_name': fields.String(required=True,
                                 help='The name of the editor'),
    'address': fields.String(required=True,
                             help='The address of the editor')
})


@editor_ns.route('/')
class EditorAPI(Resource):

    @editor_ns.doc(editor_model, description="Add a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        # Create a unique and simple ID
        editor_id = random.randint(10000, 99999)
        # Check if ID already exists
        while any(editor.editor_id == editor_id for editor in Agency.get_instance().editors):
            editor_id = random.randint(10000, 99999)

        # create a new editor object and add it
        new_editor = Editor(editor_id=editor_id,
                            editor_name=editor_ns.payload['name'],
                            address=editor_ns.payload['address'])
        Agency.get_instance().add_editor(new_editor)

        # return the new editor
        return new_editor

    @editor_ns.marshal_list_with(editor_model, envelope='editor')
    def get(self):
        return Agency.get_instance().all_editor()


@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('editor_name', type=str, required=False, help="The name of the editor")
    parser.add_argument('address', type=str, required=False, help="The address of the editor")

    @editor_ns.doc(description="Get a new editor")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        # Manage the situation when the editor is not found
        if search_result is None:
            # 404 is used for 'Not found'
            abort(404, message=f"No editor with ID {editor_id} found")
        return search_result

    @editor_ns.doc(description="Update a new editor")
    @editor_ns.expect(parser, validate=False)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self, editor_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_editor(editor_id)
        if not search_result:
            abort(404, message=f"No editor with the ID {editor_id} was found")

        updated = False
        if arguments['editor_name'] is not None:
            search_result.name = arguments['editor_name']
            updated = True
        if arguments['address'] is not None:
            search_result.address = arguments['address']
            updated = True

        if not updated:
            abort(400, message=f"No updates have been made")

        return search_result

    @editor_ns.doc(description="Delete a new editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        Agency.get_instance().remove_editor(targeted_editor)
        return jsonify(f"Editor with ID {editor_id} was removed")
