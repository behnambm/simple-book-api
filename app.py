from flask import Flask
from flask_restful import Api
from models import db
from config import Development
from resources.auth import UserRegister

app = Flask(__name__)
app.config.from_object(Development)

api = Api(app)

db.init_app(app)

# add all resources to application
api.add_resource(
    UserRegister,
    '/register',
    '/register/'
)
