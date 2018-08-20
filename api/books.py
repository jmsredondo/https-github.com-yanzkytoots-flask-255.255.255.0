# Books Controller #
from flask import request, jsonify
from app.models import *
from api import mod


@mod.route("/book", methods=["POST"])
# Create a book
def book_add():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    description = request.form.get('description')

    new_book = Book(book_name, author, description)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'OK'}), 200


@mod.route("/book", methods=["GET"])
# Get all books
def book_get():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result.data), 200


@mod.route("/book/<pk>", methods=["GET"])
# Get a specific book
def book_detail(pk):
    book = Book.query.get(pk)
    return book_schema.jsonify(book), 200


@mod.route("/book/<pk>", methods=["PUT"])
# Edit a specific book's details
def book_update(pk):
    book = Book.query.get(pk)
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    description = request.form.get('description')

    book.book_name = book_name
    book.author = author
    book.description = description

    db.session.commit()
    return book_schema.jsonify(book), 200


@mod.route("/book/<pk>", methods=["DELETE"])
# Delete a book
def book_delete(pk):
    book = Book.query.get(pk)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book), 200
