from flask import Flask
from flask_restful import Api
from models import db
from config import Development

app = Flask(__name__)
app.config.from_object(Development)

api = Api(app)

db.init_app(app)
