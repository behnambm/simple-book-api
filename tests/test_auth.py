import unittest2 as unittest
from tests.test_base import BaseTestCase
import json
from models.user import User


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


class TestUserRegister(BaseTestCase):
    def setUp(self):
        super(TestUserRegister, self).setUp()
        populate_database()
        self.user_data = {
            'first_name': 'user_first_name',
            'last_name': 'user_last_name',
            'email': 'user@email.com',
            'password': '123'
        }

    def test_register_user(self):

        response = self.app.post(
            '/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(201, response.status_code)

        self.assertTrue('message' in data)
        self.assertTrue('registration was successfull.' in data['message'])

    def test_register_with_invalid_credentials(self):
        user_data = self.user_data
        user_data['first_name'] = ''

        response = self.app.post(
            '/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

    def test_register_with_invalid_email(self):
        user_data = self.user_data
        user_data['email'] = 'test_mail'

        response = self.app.post(
            '/register',
            data=json.dumps(user_data)
        )

        self.assertEqual(400, response.status_code)

    def test_two_users_cannot_register_with_same_email(self):
        user_data = {
            'first_name': 'hugo',
            'last_name': 'alfred',
            'email': 'hugo_alfred@email.com',
            'password': '123'
        }
        response = self.app.post(
            '/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue('message' in data)
        self.assertTrue("'hugo_alfred@email.com' already exists" in data['message']) # noqa


if __name__ == '__main__':
    unittest.main()
