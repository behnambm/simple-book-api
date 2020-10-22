from config import Testing
import unittest2 as unittest
from app import create_app
from models import db


class BaseTestCase(unittest.TestCase):
    """A base test case"""
    def setUp(self):
        app = create_app(Testing)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/test_db.sqlite' # noqa

        with app.app_context():
            "To initiate testing database"
            db.create_all()

        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        db.drop_all()
