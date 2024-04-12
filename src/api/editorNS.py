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
                            editor_name=editor_ns.payload['editor_name'],
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

    @editor_ns.doc(description="Get an editor's information")
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
            search_result.editor_name = arguments['editor_name']
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
        # When an editor is removed, transfer all issues to another editor of the same newspaper
        Agency.get_instance().transfer_issues(targeted_editor)
        Agency.get_instance().remove_editor(targeted_editor)
        return jsonify(f"Editor with ID {editor_id} was removed")


# In order to handle the transfer of issues of the same newspaper, I consider adding this:
@editor_ns.route('/<int:editor_id>/newspapers')
class EditorNewspapers(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('paper_id', type=int, required=True, help='The unique identifier of a newspaper')

    @editor_ns.doc(description="Assign a newspaper to editor")
    @editor_ns.expect(parser, validate=True)
    def post(self, editor_id):
        arguments = self.parser.parse_args()
        paper_id = arguments['paper_id']

        try:
            Agency.get_instance().add_newspaper_to_editor(paper_id, editor_id)
            return jsonify(f"Newspaper with ID {paper_id} was assigned to editor with ID {editor_id}")
        except ValueError as err:
            message = str(err)
            # The newspaper doesn't exist
            if "newspaper" in message:
                abort(404, message=message)
            else:
                # The editor doesn't exist
                abort(404, message=message)


@editor_ns.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    @editor_ns.doc(description="List all newspaper issues that the editor is responsible for")
    def get(self, editor_id):
        search_result = Agency.get_instance().editor_issues(editor_id)
        if search_result is None:
            abort(404, message=f"No editor with ID {editor_id} found")

        # TypeError: Object of type Issue is not JSON serializable
        # Format each issue object into a dictionary

        issues = []
        for issue in search_result:
            issue_dict = {
                'issue_id': issue.issue_id,
                'release_date': issue.release_date,
                'number_of_pages': issue.number_of_pages,
                'released': issue.released,
                'editor_id': issue.editor_id
            }
            issues.append(issue_dict)

        if not issues:
            return jsonify(f"No issues found for editor with ID {editor_id}")

        return jsonify(issues)
