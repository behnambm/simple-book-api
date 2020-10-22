from flask_restful import Api
from resources.auth import UserRegister

api = Api()

# add all resources to application
api.add_resource(
    UserRegister,
    '/register',
    '/register/'
)
