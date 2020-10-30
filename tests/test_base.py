from config import Testing
import unittest2 as unittest
from app import create_app
from models import db
from models import Role, UserRoles, User, Book, BlackList
import json


def populate_database():
    user_list = [
        {
            'first_name': 'Ben',
            'last_name': 'blake',
            'email': 'ben_blake@email.com'
        },
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john_smith@email.com'
        },
        {
            'first_name': 'hugo',
            'last_name': 'alfred',
            'email': 'hugo_alfred@email.com'
        },
    ]
    for user in user_list:
        'This is only for populating database.'
        tmp_user = User(
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            password='123'
        )
        tmp_user.save()

    db.session.add(Role(name='user'))
    db.session.add(Role(name='author'))
    db.session.add(Role(name='admin'))

    # Populate database with fake Books
    for i in range(1, 4):
        db.session.add(
            Book(
                name=f'WonderLand {i}',
                publish_date=f'2020-02-2{i}',
                price=23.50,
                author_id=2
            )
        )

    db.session.add(UserRoles(user_id=1, role_id=1))
    db.session.add(UserRoles(user_id=2, role_id=2))
    db.session.add(UserRoles(user_id=3, role_id=3))
    db.session.commit()


class BaseTestCase(unittest.TestCase):
    """A base test case"""
    def setUp(self):
        app = create_app(Testing)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/test_db.sqlite' # noqa

        with app.app_context():
            "To initiate testing database"
            db.create_all()
            populate_database()

        app.app_context().push()
        self.app = app.test_client()

        # declare different types of users to be used in further tests
        fake_users_default_password = '123'

        self.regular_user_data = {
            'email': 'ben_blake@email.com',
            'password': fake_users_default_password
        }

        self.author_user_data = {
            'email': 'john_smith@email.com',
            'password': fake_users_default_password
        }

        self.admin_user_data = {
            'email': 'hugo_alfred@email.com',
            'password': fake_users_default_password
        }

    def login(self, data):
        """
        do login with flask test_client and return response object
        """
        response = self.app.get(
            '/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        return response

    def get_authorization_header(self, response):
        """
        return a proper http header to be acceptable as a jwt
        """
        data = json.loads(response.data)
        return {'Authorization': f"Bearer {data['access_token']}"}

    def get_access_token(self, response):
        data = json.loads(response.data)

        return data['access_token']


    def logout(self, header):
        response = self.app.get(
            '/logout',
            headers=header
        )
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue('successfully logged out' in data.get('message'))

    def tearDown(self):
        db.drop_all()
