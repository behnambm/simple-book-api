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
from models import User
from resources.book import Book


api = Api()
jwt_manager = JWTManager()


@jwt_manager.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.get_user_by_id(identity)
    if user:
        user_roles = [role.name for role in user.roles]
        return {'role': user_roles}
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

api.add_resource(
    Book,
    '/book/<int:book_id>',
    '/book/<int:book_id>/',
    '/book',
    '/book/'
)
