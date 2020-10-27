from tests.test_base import BaseTestCase
import json


class TestUserRegister(BaseTestCase):
    def setUp(self):
        super(TestUserRegister, self).setUp()
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


class TestUseLogin(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {
            'email': 'hugo_alfred@email.com',
            'password': '123'
        }

    def test_user_login(self):
        response = super().login(data=self.user_data)

        data = json.loads(response.data)


        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)
        self.assertTrue('refresh_token' in data)

    def test_invalid_email(self):
        user_data = self.user_data.copy()
        user_data['email'] = 'unknown@mail.com'

        response = super().login(data=user_data)

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('message' in data)
        self.assertTrue("couldn't find your account" in data['message'])

    def test_wrond_password(self):
        user_data = self.user_data.copy()
        user_data['password'] = '12345'

        response = super().login(data=user_data)

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('message' in data)
        self.assertTrue('invalid email or password' in data['message'])


class TestChangePassword(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.user_data = {
            'email': 'hugo_alfred@email.com',
            'password': '123'
        }

        login_response = super().login(data=self.user_data)

        self.access_token = super().get_access_token(login_response)

        self.header = super().get_authorization_header(login_response)

    def test_change_password(self):
        user_data = self.user_data.copy()
        user_data['password'] = 'new_password'

        response = self.app.put(
            '/change-password',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=self.header
        )

        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('your password successfully changed' in data['message']) # noqa

    def test_cannot_change_password_with_wrong_email(self):
        user_data = self.user_data.copy()
        user_data['email'] = 'some_wrong@email.com'

        response = self.app.put(
            '/change-password',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=self.header
        )

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('invalid credentials' in data['message'])

    def test_cannot_change_password_with_invalid_jwt(self):
        # invalid Authorization header
        header = self.header.copy()
        header['Authorization'] = 'Bearer sdf{}'.format(self.access_token)

        response = self.app.put(
            '/change-password',
            data=json.dumps(self.user_data),
            content_type='application/json',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(422, response.status_code)
        self.assertTrue('Invalid header string' in data['msg'])


class TestUserInfo(BaseTestCase):
    def setUp(self):
        super().setUp()

        login_response = super().login(data=self.admin_user_data)


        self.header = super().get_authorization_header(response=login_response)

    def test_get_user_info(self):
        response = self.app.get(
            '/user-info/',
            headers=self.header
        )
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue('info' in data)
        self.assertTrue('email' in data['info'])
        self.assertTrue('hugo_alfred@email.com' in data['info']['email'])
        self.assertTrue('admin' in data['info']['roles'])


class TestUserDelete(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.user_data = {
            'email': 'hugo_alfred@email.com',
            'password': '123'
        }
        response = super().login(data=self.user_data)

        self.header = super().get_authorization_header(response)

    def test_delete_user(self):
        response = self.app.delete(
            '/delete-account',
            headers=self.header
        )

        data = json.loads(response.data)

        self.assertEqual(202, response.status_code)
        self.assertTrue('account successfully deleted' in data['message'])

    def test_that_we_get_error_when_a_user_is_already_deleted(self):
        # first request to delete user
        response = self.app.delete(
            '/delete-account',
            headers=self.header
        )
        # second request to delete user
        response = self.app.delete(
            '/delete-account',
            headers=self.header
        )

        data = json.loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertTrue('user not found' in data['message'])
