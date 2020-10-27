from flask_restful import reqparse
from utils.common import string


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
