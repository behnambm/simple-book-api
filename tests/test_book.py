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
