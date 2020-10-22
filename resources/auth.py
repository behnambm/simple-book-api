from flask_restful import Resource, reqparse
from models.user import User
from util import email

req_parser = reqparse.RequestParser()

req_parser.add_argument(
    'first_name',
    required=True,
    help='first name is required'
)
req_parser.add_argument(
    'last_name',
    required=True,
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
    help='Passwrod field is required for registration.'
)


class UserLogin(Resource):
    def get(self):
        pass


class UserRegister(Resource):
    def post(self):
        data = req_parser.parse_args()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        new_user.save()
        return {'message': 'registration was successfull.'}, 201
