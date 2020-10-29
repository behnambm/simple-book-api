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
        self.assertTrue("only 'admin' roles allowed" in data['message'])


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

    def test_user_update_works_fine(self):
        response = self.login(self.author_user_data)
        header = self.get_authorization_header(response)

        user_data = {
            'first_name': 'A new first name'
        }

        response = self.app.put(
            '/author',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        print(data)
        self.assertTrue('A new first name' in data.get('first name'))

    def test_author_not_found_in_updating_author(self):
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.app.put(
            '/author/',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertTrue('this user is not an author' in data.get('message'))

    def test_user_not_found_works_fine_in_delete_user(self):
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/author/5',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertTrue('user not found' in data.get('message'))

    def test_admin_can_delete_authors(self):
        response = self.login(self.admin_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/author/2/',
            headers=header
        )

        self.assertEqual(204, response.status_code)

    def test_an_author_cannot_delete_another_authors_account(self):
        """
        first of all i need to add Author role to regular user
        and then i can check that i can i delete the other author's accout ot not
        """
        response = self.login(self.admin_user_data)
        header = self.get_authorization_header(response)

        # request to add Author role to regular user
        response = self.app.post(
            '/author',
            data=json.dumps({'email': self.regular_user_data['email']}),
            content_type='application/json',
            headers=header
        )

        self.assertEqual(200, response.status_code)


        # now we try to delete the other author's account
        response = self.login(self.author_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/author/1',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('you are not allowed to delete this account' in data.get('message'))


    def test_a_regular_user_cannot_delete_other_account(self):
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/author/2',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('you are not allowed to delete this account' in data.get('message'))

    def test_we_cannot_delete_a_none_author_account(self):
        response = self.login(self.admin_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/author/1',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertTrue('this user is not an author' in data.get('message'))
