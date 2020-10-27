from flask_restful import Resource, marshal, fields
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required, jwt_optional
from models.user import Book as BookModel
from util import book_req_parser, role_required
from resources.user import user_output_fields


user_output_fields.pop('roles')

book_output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'publish_date': fields.String,
    'price': fields.Float
}



class Book(Resource):
    @jwt_optional
    def get(self, book_id):
        book = BookModel.get_book_by_id(book_id=book_id)

        if not book:
            return {'message': 'book not found'}, 404

        user_output_fields_ = user_output_fields.copy()
        book_output_fields_ = book_output_fields.copy()

        if not get_jwt_identity():
            user_output_fields_.pop('email')

        book_output_fields_['author'] = fields.Nested(user_output_fields_)

        return marshal(book, book_output_fields_)

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

        return data

    def put(self):
        pass

    def delete(self):
        pass
