from flask_restful import reqparse
from utils.common import string
from flask_restful import fields


# request parser for Book Model Objects
book_req_parser = reqparse.RequestParser()

book_req_parser.add_argument(
    'name',
    required=True,
    type=string
)

book_req_parser.add_argument(
    'publish_date',
    required=True,
    type=str
)

book_req_parser.add_argument(
    'price',
    required=True,
    type=float
)


BOOK_OUTPUT_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'publish_date': fields.String,
    'price': fields.Float
}
