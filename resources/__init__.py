from flask_restful import Api
from resources.auth import UserRegister, UserLogin
from flask_jwt_extended import JWTManager

api = Api()
jwt_manager = JWTManager()

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
