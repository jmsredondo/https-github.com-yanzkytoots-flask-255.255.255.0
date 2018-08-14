from flask import jsonify, request
from app import app
from app.models import *


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route("/book", methods=["POST"])
def book_add():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    description = request.form.get('description')

    new_book = Book(book_name, author, description)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'OK'}), 200


@app.route("/book", methods=["GET"])
def book_get():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify({'message': 'OK'}), 200


@app.route("/book/<pk>", methods=["GET"])
def book_detail(pk):
    book = Book.query.get(pk)
    return book_schema.jsonify(book)


@app.route("/book/<pk>", methods=["PUT"])
def book_update(pk):
    book = Book.query.get(pk)
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    description = request.form.get('description')

    book.book_name = book_name
    book.author = author
    book.description = description

    db.session.commit()
    return book_schema.jsonify(book)


@app.route("/book/<pk>", methods=["DELETE"])
def book_delete(pk):
    book = Book.query.get(pk)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)