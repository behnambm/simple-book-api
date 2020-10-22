from flask_restful import Resource, reqparse
from models.user import User
from util import email

req_parser = reqparse.RequestParser()

req_parser.add_argument(
    'username',
    required=True,
    help='Username field is required for registration.'
)
req_parser.add_argument(
    'email',
    required=True,
    type=email,
    help='Email field is required for registration.'
)
req_parser.add_argument(
    'password',
    required=True,
    help='Passwrod field is required for registration.'
)


class UserLogin(Resource):
    def get(self):
        pass


class UserRegister(Resource):
    def post(self):
        data = req_parser.parse_args()
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        new_user.save()
        return {'message': 'Registration was successfull.'}
