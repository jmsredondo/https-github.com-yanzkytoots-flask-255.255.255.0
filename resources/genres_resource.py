from flask_restful import Resource, reqparse
from app.models import *

# ------------------------------ PARSE INPUTS ------------------------------ #
genre_parser = reqparse.RequestParser(bundle_errors=True)
genre_parser.add_argument('genre', help='This field cannot be blank', required=True)
genre_parser.add_argument('type', help='This field cannot be blank', required=True)

id_parser = reqparse.RequestParser()
id_parser.add_argument('book_id', required=True)


# ------------------------------ ROUTE: /genre ------------------------------ #
class GenreMethods(Resource):
    def get(self):
        # Retrieve all genres #
        return Genre.get_all()

    def delete(self):
        # Delete all genres #
        return Genre.delete_all()

    def post(self):
        # Create a genre #
        data = genre_parser.parse_args()

        if Genre.find_by_name(data['genre']) and Genre.find_by_type(data['type']):
            return {
                       'message': 'This genre already exists in the database'
                   }, 202

        new_genre = Genre(
            genre=data['genre'],
            type=data['type']
        )

        try:
            new_genre.save_to_db()
            return {
                       'message': 'Genre successfully added'
                   }, 200

        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


# ------------------------------ ROUTE: /genre/<pk> ------------------------------ #
class GenreDetailMethods(Resource):
    # Retrieve a genre #
    def get(self, pk):
        if Genre.find_by_id(pk):
            return Genre.detail(pk)
        else:
            return {
                       'message': 'Genre not found'
                   }, 404

    # Delete a genre #
    def delete(self, pk):
        if Genre.find_by_id(pk):
            try:
                Genre.delete(pk)
                return {
                           'message': 'Genre successfully deleted'
                       }, 200
            except:
                return {
                           'message': 'Authentication information is missing or invalid'
                       }, 401

        else:
            return {
                       'message': 'Genre not found'
                   }, 404

    # Update an existing genre's information #
    def put(self, pk):
        data = genre_parser.parse_args()

        if not Genre.find_by_id(pk):
            return {
                       'message': 'Genre not found'
                   }, 404
        elif Genre.find_by_name(data['genre']) and Genre.find_by_type(data['type']):
            return {
                       'message': 'This genre already exists in the database'
                   }, 202

        new_genre = Genre(
            genre=data['genre'],
            type=data['type']
        )

        try:
            Genre.update(new_genre, pk)
            return {
                       'message': 'Successfully updated genre information'
                   }, 200
        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


# ------------------------------ ROUTE: /genre/addbook/<pk> ------------------------------ #
class GenreBookMethods(Resource):
    # Retrieve all books from a genre #
    def get(self, pk):
        if Genre.find_by_id(pk):
            return Genre.get_all_books(pk)
        else:
            return {
                       'message': 'Genre not found'
                   }, 404

        # Add a book to a genre #

    def post(self, pk):
        data = id_parser.parse_args()
        if Category.find_by_book(data['book_id']) and Category.find_by_genre(pk):
            return {
                       'message': 'Book being added already exists in this genre'
                   }, 202
        try:
            Genre.add_book(data['book_id'], pk)
            return {
                       'message': 'Successfully added book to this genre'
                   }, 200
        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401
