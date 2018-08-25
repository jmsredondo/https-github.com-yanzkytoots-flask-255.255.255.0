from flask_restful import Resource, reqparse
from app.models import *

genre_parser = reqparse.RequestParser(bundle_errors=True)
genre_parser.add_argument('genre', help='This field cannot be blank', required=True)
genre_parser.add_argument('type', help='This field cannot be blank', required=True)

id_parser = reqparse.RequestParser()
id_parser.add_argument('book_id', required=True)


class GenreMethods(Resource):
    def get(self):
        return Genre.get_all()

    def delete(self):
        return Genre.delete_all()

    def post(self):
        data = genre_parser.parse_args()

        if Genre.find_by_name(data['genre']) and Genre.find_by_type(data['type']):
            return {'message': 'The genre {} already exists'.format(data['genre'])}

        new_genre = Genre(
            genre=data['genre'],
            type=data['type']
        )
        try:
            new_genre.save_to_db()
            return {
                'genre': '{}'.format(data['genre']),
                'type': '{}'.format(data['type']),
            }, 200

        except:
            return {
                'message': 'Authentication information is missing or invalid'
            }, 401


class GenreDetailMethods(Resource):
    def get(self, pk):
        if Genre.find_by_id(pk):
            return Genre.detail(pk)
        else:
            return {
                'message': 'Genre not found'
            }, 404

    def post(self, pk):
        return Genre.update(pk)

    def delete(self, pk):
        return Genre.delete(pk)

    def put(self, pk):
        data = genre_parser.parse_args()

        if Genre.find_by_name(data['genre']) and Genre.find_by_type(data['type']):
            return {'message': 'The genre {} already exists'.format(data['genre'])}

        new_genre = Genre(
            genre=data['genre'],
            type=data['type']
        )
        try:
            Genre.update(new_genre, pk)
            return {
                'genre': '{}'.format(data['genre']),
                'type': '{}'.format(data['type']),
            }, 200
        except:
            return {
                'message': 'Authentication information is missing or invalid'
            }, 401


class GenreBookMethods(Resource):
    def get(self, pk):
        if Genre.find_by_id(pk):
            return Genre.get_all_books(pk)
        else:
            return {
                'message': 'Genre not found'
            }, 404

    def post(self, pk):
        data = id_parser.parse_args()
        """if Genre.find_by_book(data['book_id']):
            return {'message': 'Book being added already exists in this genre'}"""
        try:
            Genre.add_book(data['book_id'], pk)
            return{
                'genre_id': '{}'.format(pk),
                'book_id': '{}'.format(data['book_id']),
            }, 200
        except:
            return {
                'message': 'Authentication information is missing or invalid'
            }, 401
