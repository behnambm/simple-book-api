from flask import Flask
from models import db
from config import Development
from resources import api, jwt_manager


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    api.init_app(app)
    jwt_manager.init_app(app)
    return app


app = create_app(Development)
