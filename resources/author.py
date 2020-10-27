from flask_restful import Resource, reqparse, fields, marshal
from utils.common import email
from utils.user import role_required
from models import User
from flask_jwt_extended import fresh_jwt_required


req_parser = reqparse.RequestParser()

req_parser.add_argument(
    'email',
    type=email,
    required=True
)

user_output_fields = {
    'first name': fields.String(attribute='first_name'),
    'last name': fields.String(attribute='last_name'),
    'email': fields.String,
    'roles': fields.List(fields.String(attribute='name'))
}


class Author(Resource):
    @fresh_jwt_required
    @role_required('admin')
    def post(self):
        data = req_parser.parse_args()
        user = User.get_user_by_email(data['email'])

        if not user:
            return {'message': 'user not found'}, 404

        if user.has_role('author'):
            return {'message': "this account already has 'Author' privilege"}, 409

        if not user.has_role('author'):
            user.add_role('author')
            output_fields = user_output_fields.copy()
            output_fields['message'] = fields.FormattedString('role added to the account') # noqa
            return marshal(user, output_fields)

    def get(self, user_id):
        user = User.get_user_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404

        if user.has_role('author'):
            return marshal(user, user_output_fields)

        return {'message': 'author not found'}, 404


    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass
