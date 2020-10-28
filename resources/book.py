from flask_restful import Resource, marshal, fields
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_optional
from models import Book as BookModel
from utils.book import book_req_parser, BOOK_OUTPUT_FIELDS
from utils.user import role_required, USER_OUTPUT_FIELDS


class Book(Resource):
    @jwt_optional
    def get(self, book_id):
        book = BookModel.get_book_by_id(book_id=book_id)

        if not book:
            return {'message': 'book not found'}, 404

        user_outputs = USER_OUTPUT_FIELDS.copy()
        user_outputs.pop('roles')  # to not show roles in this endpoint

        book_outputs = BOOK_OUTPUT_FIELDS.copy()

        if not get_jwt_identity():
            user_outputs.pop('email')

        book_outputs['author'] = fields.Nested(user_outputs)

        return marshal(book, book_outputs)

    @fresh_jwt_required
    @role_required('author')
    def post(self):
        data = book_req_parser.parse_args()

        book = BookModel(
            name=data.get('name'),
            publish_date=data.get('publish_date'),
            price=data.get('price'),
            author_id=get_jwt_identity()
        )
        book.save()

        output_fields = BOOK_OUTPUT_FIELDS.copy()
        output_fields['message'] = fields.FormattedString('book successfully created')

        return marshal(book, BOOK_OUTPUT_FIELDS), 201


    @fresh_jwt_required
    def put(self, book_id):
        data = book_req_parser.parse_args()

        book = BookModel.get_book_by_id(book_id)

        if not book:
            return {'message': 'book not found'}, 404

        if book.author.id != get_jwt_identity():
            return {'message': 'you are not allowed to update this book'}, 401

        book.name = data.get('name')
        book.publish_date = data.get('publish_date')
        book.price = data.get('price')

        book.save()

        output_fields = BOOK_OUTPUT_FIELDS.copy()
        output_fields['message'] = fields.FormattedString('book has been updated')

        return marshal(book, BOOK_OUTPUT_FIELDS), 200


    @fresh_jwt_required
    def delete(self, book_id):
        book = BookModel.get_book_by_id(book_id)

        if not book:
            return {'message': 'book not found'}, 404

        if book.author.id != get_jwt_identity():
            return {'message': 'you are not allowed to delete this book'}, 401

        book.delete()

        return {'message': 'book successfully deleted'}, 202
