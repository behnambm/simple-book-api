from flask_restful import Resource, reqparse, fields, marshal
from utils.common import email
from utils.user import role_required, USER_OUTPUT_FIELDS, none_required_req_parser
from models import User
from flask_jwt_extended import fresh_jwt_required, jwt_optional, get_jwt_identity, get_jwt_claims
from utils.book import BOOK_OUTPUT_FIELDS


req_parser = reqparse.RequestParser()

req_parser.add_argument(
    'email',
    type=email,
    required=True
)


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
            output_fields = USER_OUTPUT_FIELDS.copy()
            output_fields['message'] = fields.FormattedString('role added to the account') # noqa

            return marshal(user, output_fields)

    @jwt_optional
    def get(self, user_id):
        user = User.get_user_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404

        if not user.has_role('author'):
            return {'message': 'author not found'}, 404

        output_fields = USER_OUTPUT_FIELDS.copy()
        output_fields['books'] = fields.List(fields.Nested(BOOK_OUTPUT_FIELDS))

        if not get_jwt_identity():
            output_fields.pop('email')
            output_fields.pop('roles')
            return marshal(user, output_fields)

        return marshal(user, output_fields)


    @fresh_jwt_required
    def put(self):
        req_parser = none_required_req_parser.parse_args()

        user = User.get_user_by_id(get_jwt_identity())

        if not user:
            return {'message': 'user not found'}, 404

        if not user.has_role('author'):
            return {'message': 'this user is not an author'}, 400

        user.first_name = req_parser.get('first_name') or user.first_name
        user.last_name = req_parser.get('last_name') or user.last_name
        user.email = req_parser.get('email') or user.email

        user.save()
        return marshal(user, USER_OUTPUT_FIELDS)


    @fresh_jwt_required
    def delete(self, user_id):
        user = User.get_user_by_id(user_id)

        if not user:
            return {'message': 'user not found'}, 404

        current_user_roles = get_jwt_claims().get('role')

        if 'admin' in current_user_roles:
            user.delete()
            return {'message': 'account successfully deleted'}, 204

        if 'author' in current_user_roles:
            if user.id == get_jwt_identity():
                user.delete()
                return {'message': 'account successfully deleted'}, 204

        return {'message': 'you are not allowed to delete this account'}, 401
