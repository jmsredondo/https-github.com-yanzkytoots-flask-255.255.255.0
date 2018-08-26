from flask_restful import Resource, reqparse
from app.models import *

# ------------------------------ PARSE INPUTS ------------------------------ #
book_parser = reqparse.RequestParser(bundle_errors=True)
book_parser.add_argument('book_name', help='This field cannot be blank', required=True)
book_parser.add_argument('author', help='This field cannot be blank', required=True)
book_parser.add_argument('description', required=False)

rating_parser = reqparse.RequestParser(bundle_errors=True)
rating_parser.add_argument('book_id', help='This field cannot be blank', required=True)
rating_parser.add_argument('user_id', help='This field cannot be blank', required=True)
rating_parser.add_argument('rate', type=int, help='This field cannot be blank', required=True)
rating_parser.add_argument('comment', required=False)


# ------------------------------ ROUTE: /book ------------------------------ #
class BookMethods(Resource):
    # Retrieve all books #
    def get(self):
        return Book.get_all()

    # Delete all books #
    def delete(self):
        return Book.delete_all()

    # Create a book #
    def post(self):
        data = book_parser.parse_args()

        if Book.find_by_book_name(data['book_name']) and Book.find_by_author(data['author']):
            return {
                       'message': 'This book already exists in the database'
                   }, 202

        new_book = Book(
            book_name=data['book_name'],
            author=data['author'],
            description=data['description']
        )

        try:
            new_book.save_to_db()
            return {
                       'message': 'Book successfully added'
                   }, 200

        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


# ------------------------------ ROUTE: /book/<pk> ------------------------------ #
class BookDetailMethods(Resource):
    # Retrive a book #
    def get(self, pk):
        if Book.find_by_id(pk):
            return Book.detail(pk)
        else:
            return {
                       'message': 'Book not found'
                   }, 404

    # Delete a book #
    def delete(self, pk):
        if Book.find_by_id(pk):
            try:
                Book.delete(pk)
                return {
                           'message': 'Book successfully deleted'
                       }, 200
            except:
                return {
                           'message': 'Authentication information is missing or invalid'
                       }, 401
        else:
            return {
                        'message': 'Book not found'
                    }, 404

    # Update an existing book's information #
    def put(self, pk):
        data = book_parser.parse_args()

        if not Book.find_by_id(pk):
            return {
                       'message': 'Book not found'
                   }, 404
        elif Book.find_by_book_name(data['book_name']) and Book.find_by_author(data['author']):
            return {
                       'message': 'This book already exists in the database'
                   }, 202

        new_book = Book(
            book_name=data['book_name'],
            author=data['author'],
            description=data['description']
        )

        try:
            Book.update(new_book, pk)
            return {
                       'message': 'Successfully updated book information'
                   }, 200

        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


# ------------------------------ ROUTE: /rate ------------------------------ #
class BookRateMethods(Resource):
    # Rate a book #
    def post(self):
        data = rating_parser.parse_args()

        if Rating.find_by_user(data['user_id']) and Rating.find_by_book(data['book_id']):
            return {
                       'message': 'User has already rated this book'
                   }, 202
        elif not Book.find_by_id(data['book_id']):
            return {
                       'message': 'Book not found'
                   }, 404
        elif not User.find_by_id(data['user_id']):
            return {
                       'message': 'User not found'
                   }, 404

        new_rating = Rating(
            book_id=data['book_id'],
            user_id=data['user_id'],
            comment=data['comment'],
            rate=data['rate']
        )

        try:
            Rating.save_to_db(new_rating)
            return {
                       'message': 'Thank you for your feedback!'
                   }, 200
        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


# ------------------------------ ROUTE: /rate/<pk> ------------------------------ #
class BookRateDetailMethods(Resource):
    # Retrieve all ratings for a book #
    def get(self, pk):
        if Book.find_by_id(pk):
            return Book.get_all_ratings(pk)
        else:
            return {
                       'message': 'Book not found'
                   }, 404
