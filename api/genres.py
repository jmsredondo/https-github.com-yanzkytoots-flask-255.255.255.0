# Genres Controller #
from flask import request, jsonify
from app.models import *
from api import app


@app.route("/genre", methods=["POST"])
# Add a genre
def genre_add():
    genre_name = request.form.get('genre')
    type = request.form.get('type')

    new_genre = Genre(genre_name, type)
    db.session.add(new_genre)
    db.session.commit()

    return jsonify({'message': 'OK'}), 200


@app.route("/genre", methods=["GET"])
# Get all genres
def genre_get():
    all_genres = Genre.query.all()
    result = genres_schema.dump(all_genres)
    return jsonify(result.data), 200


@app.route("/genre/<pk>", methods=["PUT"])
# Edit a specific genre's details
def genre_update(pk):
    genre = Genre.query.get(pk)
    genre_name = request.form.get('genre')
    type = request.form.get('type')

    genre.genre = genre_name
    genre.type = type

    db.session.commit()
    return genre_schema.jsonify(genre), 200


@app.route("/genre/<pk>", methods=["DELETE"])
# Delete a genre
def genre_delete(pk):
    genre = Genre.query.get(pk)
    db.session.delete(genre)
    db.session.commit()

    return genre_schema.jsonify(genre), 200


@app.route("/genre/addbook/<pk>", methods=["POST"])
# Add a book to a genre
def genre_addbook(pk):
    genre = Genre.query.get(pk)
    book_id = request.form.get('id')
    book = Book.query.get(int(book_id))

    genre.books.append(book)
    db.session.add(genre)
    db.session.commit()

    return genre_schema.jsonify(genre), 200


@app.route("/genre/<pk>", methods=["GET"])
# View books by category
def genre_detail(pk):
    genre = Genre.query.get(pk)
    all_books = genre.books

    return books_schema.jsonify(all_books)
