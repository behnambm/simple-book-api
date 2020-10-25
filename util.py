from email_validator import validate_email
from functools import wraps
from flask_jwt_extended import get_jwt_claims


def email(_email):
    "This is going to be used in request parser arguments"
    if validate_email(_email, check_deliverability=False):
        return _email


def string(value):
    "This will be used in request parser as a type"
    value = value.strip()
    if value != '':
        return value

    raise 'Not a valid string'


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_jwt_claims().get('is_admin'):
            return {'message': 'only admins allowed'}, 401

        return func(*args, **kwargs)
    return wrapper
