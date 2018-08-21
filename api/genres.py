# Genres Controller #
from flask import request
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

    response = genre_schema.jsonify(new_genre)
    response.status_code = 200
    return response


@app.route("/genre", methods=["GET"])
# Get all genres
def genre_get():
    all_genres = Genre.query.all()
    response = genres_schema.jsonify(all_genres)
    response.status_code = 200
    return response


@app.route("/genre/<pk>", methods=["GET"])
# Get a specific genre
def genre_detail(pk):
    genre = Genre.query.get(pk)
    response = genre_schema.jsonify(genre)
    response.status_code = 200
    return response


@app.route("/genre/<pk>", methods=["PUT"])
# Edit a specific genre's details
def genre_update(pk):
    genre = Genre.query.get(pk)
    genre_name = request.form.get('genre')
    type = request.form.get('type')

    genre.genre = genre_name
    genre.type = type

    db.session.commit()

    response = genre_schema.jsonify(genre)
    response.status_code = 200
    return response


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


@app.route("/category/<pk>", methods=["GET"])
# View books by category
<<<<<<< HEAD
def genre_books(pk):
=======
def genre_detailboks(pk):
>>>>>>> 1d015bfdcd1de0992ee0ad5812e942f6601d1414
    genre = Genre.query.get(pk)
    all_books = genre.books

    return books_schema.jsonify(all_books)
