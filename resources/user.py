from flask_restful import Resource, reqparse, fields, marshal
from models import User
from utils.common import email, string
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    fresh_jwt_required,
    get_jwt_identity,
    jwt_required
)


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


class ChangePassword(Resource):
    @fresh_jwt_required
    def put(self):
        parser = req_parser.copy()
        parser.remove_argument('first_name')
        parser.remove_argument('last_name')
        data = parser.parse_args()

        identity = get_jwt_identity()
        user = User.get_user_by_id(identity)

        if user:
            if user.email == data['email']:
                user.password = data['password']
                user.save()
                return {'message': 'your password successfully changed'}, 200

            return {'message': 'invalid credentials'}, 401

        return {'message': "couldn't find your account"}, 400


user_output_fields = {
    'id': fields.Integer,
    'first name': fields.String(attribute='first_name'),
    'last name': fields.String(attribute='last_name'),
    'email': fields.String,
    'roles': fields.List(fields.String(attribute='name'))
}


class UserInfo(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        user = User.get_user_by_id(identity)
        if not user:
            return {'message': 'user not found'}, 404

        return marshal(user, user_output_fields, envelope='info')


class DeleteAccount(Resource):
    @fresh_jwt_required
    def delete(self):
        identity = get_jwt_identity()
        user = User.get_user_by_id(identity)
        if not user:
            return {'message': 'user not found'}, 404

        user.delete()
        return {'message': 'account successfully deleted'}, 202
