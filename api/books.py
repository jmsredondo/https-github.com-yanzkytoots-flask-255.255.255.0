# Books Controller #
from flask import request, jsonify
from app.models import *
from api import app


@app.route("/book", methods=["POST"])
# Create a book
def book_add():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    description = request.form.get('description')

    new_book = Book(book_name, author, description)
    db.session.add(new_book)
    db.session.commit()

    response = book_schema.jsonify(new_book)
    response.status_code = 200
    return response


@app.route("/book", methods=["GET"])
# Get all books
def book_get():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    response = jsonify(result.data)
    response.status_code = 200
    return response


@app.route("/book/<pk>", methods=["GET"])
# Get a specific book
def book_detail(pk):
    book = Book.query.get(pk)
    response = book_schema.jsonify(book)
    response.status_code = 200
    return response


@app.route("/book/<pk>", methods=["PUT"])
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

    response = book_schema.jsonify(book)
    response.status_code = 200
    return response


@app.route("/book/<pk>", methods=["DELETE"])
# Delete a book
def book_delete(pk):
    book = Book.query.get(pk)
    db.session.delete(book)
    db.session.commit()

    response = book_schema.jsonify(book)
    response.status_code = 200
    return response
