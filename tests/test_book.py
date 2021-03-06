from tests.test_base import BaseTestCase
import json


class Book(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.book_data = {
            'name': 'Harry Potter 1',
            'publish_date': '2020-10-27',
            'price': 46.60,
            'author_id': 2
        }

    def get_book_info(self, book_id, header=None):
        response = self.app.get(
            '/book/' + str(book_id),
            headers=header
        )

        return response


    def post_book(self, data, header):
        response = self.app.post(
            '/book/',
            data=json.dumps(data),
            headers=header,
            content_type='application/json'
        )

        return response


    def test_post_new_books(self):
        # get jwt tokens
        response = self.login(self.author_user_data)
        header = self.get_authorization_header(response)

        response = self.post_book(self.book_data, header)

        self.assertEqual(201, response.status_code)


    def test_get_info_with_jwt_token(self):
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.get_book_info(3, header)

        data = json.loads(response.data)

        print(data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('john_smith@email.com' in data['author']['email'])

    def test_get_book_info_without_jwt_token(self):
        response = self.get_book_info(3)

        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(data['author'].get('email'))

    def test_book_not_found(self):
        response = self.get_book_info(23)

        self.assertEqual(404, response.status_code)

    def test_none_authors_cannot_post_new_books(self):
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.post_book(self.book_data, header=header)

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue("only 'author' roles allowed" in data['message'])

    def test_update_book(self):
        response = self.login(self.author_user_data)
        header = self.get_authorization_header(response)

        book_data = self.book_data.copy()
        book_data['price'] = 68

        response = self.app.put(
            '/book/3/',
            data=json.dumps(book_data),
            content_type='application/json',
            headers=header
        )
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(68, data.get('price'))

    def test_delete_book(self):
        response = self.login(self.author_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/book/3/',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(202, response.status_code)
        self.assertTrue('book successfully deleted' in data.get('message'))

    def test_cannot_delete_book_with_none_author_user(self):
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.app.delete(
            '/book/3/',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('you are not allowed to delete this book' in data.get('message'))

    def test_cannot_update_other_authors_books(self):
        # first i add Author role to regular user
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

        # now i can check that another author can or cannot update
        # other author's book
        response = self.login(self.regular_user_data)
        header = self.get_authorization_header(response)

        response = self.app.put(
            '/book/3/',
            data=json.dumps(self.book_data),
            content_type='application/json',
            headers=header
        )

        data = json.loads(response.data)

        self.assertEqual(401, response.status_code)
        self.assertTrue('you are not allowed to update this book' in data.get('message'))
