from flask_restful import Resource, reqparse
from models.user import User
from util import email, string
from flask_jwt_extended import create_access_token, create_refresh_token


req_parser = reqparse.RequestParser()

req_parser.add_argument(
    'first_name',
    required=True,
    type=string,
    help='first name is required, {error_msg}'
)
req_parser.add_argument(
    'last_name',
    required=True,
    type=string,
    help='last name is required'
)
req_parser.add_argument(
    'email',
    required=True,
    type=email
)
req_parser.add_argument(
    'password',
    required=True,
    type=string,
    help='Passwrod field is required for registration.'
)


class UserLogin(Resource):
    def get(self):
        parser = req_parser.copy()
        parser.remove_argument('first_name')
        parser.remove_argument('last_name')
        data = parser.parse_args()
        user = User.get_user_by_email(data['email'])
        if not user:
            return {'message': 'couldn\'t find your account'}, 401

        if not user.check_password(data['password']):
            return {'message': 'invalid email or password'}, 401

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


class UserRegister(Resource):
    def post(self):
        data = req_parser.parse_args()
        user = User.get_user_by_email(data['email'])
        if user:
            return {'message': '{!r} already exists'.format(data['email'])}, 400 # noqa

        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        new_user.save()
        return {'message': 'registration was successfull.'}, 201
