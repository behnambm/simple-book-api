from flask_restful import Resource, reqparse, fields, marshal
from util import email, admin_required
from models.user import User
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
    @admin_required
    def post(self):
        data = req_parser.parse_args()
        user = User.get_user_by_email(data['email'])
        # user.roles will give us a list of Role objects
        # so we need to get names of those objects
        if not user:
            return {'message': 'user not found'}, 404

        user_roles = [role.name for role in user.roles]
        if 'author' in user_roles:
            return {'message': "this account already has 'Author' privilege"}

        if 'user' in user_roles or 'admin' in user_roles:
            user.add_role('author')
            user_output_fields['message'] = fields.FormattedString('role added to the account') # noqa
            return marshal(user, user_output_fields)
