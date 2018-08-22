from flask_restful import Resource, reqparse
from models import *

book_parser = reqparse.RequestParser(bundle_errors=True)
book_parser.add_argument('book_name', help='This field cannot be blank', required=True)
book_parser.add_argument('author', help='This field cannot be blank', required=True)
book_parser.add_argument('description', required=False)

id_parser = reqparse.RequestParser()
id_parser.add_argument('id')


class BookMethods(Resource):
    def get(self):
        return Book.get_all()

    def delete(self):
        return Book.delete_all()

    def post(self):
        data = book_parser.parse_args()

        if Book.find_by_book_name(data['book_name']) and Book.find_by_author(data['author']):
            return {'message': 'The book {} already exists'.format(data['book_name'])}

        new_book = Book(
            book_name=data['book_name'],
            author=data['author'],
            description=data['description']
        )
        try:
            new_book.save_to_db()
            return {
                'book_name': '{}'.format(data['book_name']),
                'author': '{}'.format(data['author']),
                'description': '{}'.format(data['description'])
            }, 200

        except:
            return {
                'message': 'Authentication information is missing or invalid'
            }, 401


class BookDetailMethods(Resource):
    def get(self, pk):
        if Book.find_by_id(pk):
            return Book.detail(pk)
        else:
            return {
                'message': 'Book not found'
            }, 404

    def post(self, pk):
        return Book.update(pk)

    def delete(self, pk):
        return Book.delete(pk)

    def put(self, pk):
        data = book_parser.parse_args()

        new_book = Book(
            book_name=data['book_name'],
            author=data['author'],
            description=data['description']
        )
        try:
            Book.update(new_book, pk)
            return {
                'book_name': '{}'.format(data['book_name']),
                'author': '{}'.format(data['author']),
                'description': '{}'.format(data['description']),
            }, 200
        except:
            return {
                'message': 'Authentication information is missing or invalid'
            }, 401
