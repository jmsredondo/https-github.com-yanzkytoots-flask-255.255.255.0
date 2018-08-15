from flask import jsonify, request, render_template, redirect
from app import app
from app.models import *
from werkzeug.security import generate_password_hash


@app.route('/', methods=['POST', 'GET'])
def login():
    """if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        userLogin = User.query.get(username, password)
        print(userLogin)

        return render_template('test.html')"""

    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashedpassword = generate_password_hash(password)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')

        new_user = User(username, hashedpassword, firstname, lastname, phone, email)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/#success')

    return render_template('registration.html')


# Books Controller #

@app.route("/book", methods=["POST"])
def book_add():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    description = request.form.get('description')

    new_book = Book(book_name, author, description)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'OK'})


@app.route("/book", methods=["GET"])
def book_get():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result.data), 200


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


# Genres Controller #

@app.route("/genre", methods=["POST"])
def genre_add():
    genre_name = request.form.get('genre')
    type = request.form.get('type')

    new_genre = Genre(genre_name, type)
    db.session.add(new_genre)
    db.session.commit()

    return jsonify({'message': 'OK'}), 200


@app.route("/genre", methods=["GET"])
def genre_get():
    all_genres = Genre.query.all()
    result = genres_schema.dump(all_genres)
    return jsonify(result.data)


@app.route("/genre/<pk>", methods=["PUT"])
def genre_update(pk):
    genre = Genre.query.get(pk)
    genre_name = request.form.get('genre')
    type = request.form.get('type')

    genre.genre = genre_name
    genre.type = type

    db.session.commit()
    return genre_schema.jsonify(genre), 200


@app.route("/genre/<pk>", methods=["DELETE"])
def genre_delete(pk):
    genre = Genre.query.get(pk)
    db.session.delete(genre)
    db.session.commit()

    return genre_schema.jsonify(genre), 200
