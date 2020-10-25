from flask_restful import Api
from resources.user import (
    UserRegister,
    UserLogin,
    ChangePassword,
    UserInfo,
    DeleteAccount
)
from flask_jwt_extended import JWTManager
from resources.author import Author
from models.user import User


api = Api()
jwt_manager = JWTManager()


@jwt_manager.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.get_user_by_id(identity)
    if user:
        user_roles = [role.name for role in user.roles]
        if 'admin' in user_roles:
            return {'is_admin': True}
    return None


# add all resources to application
api.add_resource(
    UserRegister,
    '/register',
    '/register/'
)

api.add_resource(
    UserLogin,
    '/login',
    '/login/'
)

api.add_resource(
    ChangePassword,
    '/change-password',
    '/change-password/'
)

api.add_resource(
    UserInfo,
    '/user-info',
    '/user-info/'
)

api.add_resource(
    DeleteAccount,
    '/delete-account',
    '/delete-account/'
)

api.add_resource(
    Author,
    '/author/<int:user_id>',
    '/author/<int:user_id>/',
    '/author',
    '/author/'
)
