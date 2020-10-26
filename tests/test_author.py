from tests.test_base import BaseTestCase
import json


class TestGrantingUserRoleToAuthor(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.admin_user_data = {
            'email': 'hugo_alfred@email.com',
            'password': '123'
        }

        self.none_admin_user_data = {
            'email': 'ben_blake@email.com',
            'password': '123'
        }

    def grant_role_to_author(self, email, header):
        """
        Grant role to author in account that email belongs to
        use header to authenticate
        the one who sends request to grant role can be either admin or regular user
        """
        user_data = {
            'email': email
        }

        response = self.app.post(
            '/author/',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=header
        )
        return response

    def test_granting_user_role_works_fine(self):
        # get jwt token with this function
        response = super().login(data=self.admin_user_data)
        # get a proper http header
        header = super().get_authorization_header(response=response)


        response = self.grant_role_to_author('ben_blake@email.com', header=header)


        data = json.loads(response.data)


        self.assertEqual(200, response.status_code)
        self.assertTrue('role added to the account' in data['message'])


    def test_cannot_grant_role_with_none_admin_user(self):
        # in here we try to login with a none ADMIN user
        response = super().login(data=self.none_admin_user_data)
        header = super().get_authorization_header(response)


        response = self.grant_role_to_author('ben_blake@email.com', header=header)


        data = json.loads(response.data)


        self.assertEqual(401, response.status_code)
        self.assertTrue('only admins allowed' in data['message'])


    def test_cannot_grant_a_user_role_twice(self):
        response = super().login(self.admin_user_data)
        header = super().get_authorization_header(response)


        # first try to grant role
        self.grant_role_to_author('ben_blake@email.com', header=header)

        # second try to grant role wheich we expect to fail
        response = self.grant_role_to_author('ben_blake@email.com', header=header)


        data = json.loads(response.data)


        self.assertEqual(409, response.status_code)
        self.assertTrue("this account already has 'Author' privilege" in data['message'])
