from functools import wraps
from flask_jwt_extended import get_jwt_claims
from flask_restful import fields


def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_jwt_claims().get('role'):

                if role_name in get_jwt_claims().get('role'):
                    return func(*args, **kwargs)

                return {'message': 'only {!r} roles allowed'.format(role_name)}, 401

            return {'message': 'jwt has no role claim'}, 400
        return wrapper
    return decorator


USER_OUTPUT_FIELDS = {
    'id': fields.Integer,
    'first name': fields.String(attribute='first_name'),
    'last name': fields.String(attribute='last_name'),
    'email': fields.String,
    'roles': fields.List(fields.String(attribute='name'))
}
