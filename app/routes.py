from flask import jsonify, request, render_template, redirect
from app import app
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


def __init__(self, username, password):
    self.username = username
    self.password = password


@app.route('/', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':

        user = User.query.all()
        for u in user:
            if u.username == username and check_password_hash(u.password, password):

                return render_template('dashboard.html', name=username)

        return redirect('/#loginFailed')
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():

    return render_template('dashboard.html')


@app.route('/users', methods=['GET'])
def users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data), 200


@app.route('/logout', methods=['GET'])
def logout():
    return render_template('index.html')


@app.route('/shookedbtn', methods=['GET'])
def shookedbtn():
    return render_template('dashboard.html')


@app.route('/gen', methods=['GET'])
def gen():
    return render_template('gen.html')


@app.route('/libr', methods=['GET'])
def libr():
    return render_template('libr.html')


@app.route('/landing', methods=['GET'])
def landing():
    return render_template('#')


@app.route('/addgenre', methods=['GET'])
def addgenre():
    return render_template('addgenre.html')

@app.route('/addbook', methods=['GET'])
def addbook():
    return render_template('addbook.html')

@app.route('/boks', methods=['GET'])
def boks():
    return render_template('boks.html')



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
<<<<<<< HEAD


# Books Controller #

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
    return jsonify(result.data), 200


@app.route("/book/<pk>", methods=["GET"])
def book_detail(pk):
    book = Book.query.get(pk)
    return book_schema.jsonify(book), 200


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
    return book_schema.jsonify(book), 200


@app.route("/book/<pk>", methods=["DELETE"])
def book_delete(pk):
    book = Book.query.get(pk)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book), 200


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
    return jsonify(result.data), 200


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


@app.route("/genre/addbook/<pk>", methods=["POST"])
def genre_addbook(pk):

    genre = Genre.query.get(pk)
    book_id = request.form.get('id')
    book = Book.query.get(int(book_id))

    genre.books.append(book)
    db.session.add(genre)
    db.session.commit()

    return genre_schema.jsonify(genre), 200


@app.route("/genre/<pk>", methods=["GET"])
def genre_detail(pk):

    genre = Genre.query.get(pk)
    all_books = genre.books

    return books_schema.jsonify(all_books)


@app.route("/library", methods=["POST"])
def library_add():

    book_id = request.form.get('book_id')
    user_id = request.form.get('id')

    user = User.query.get(user_id)
    book = Book.query.get(book_id)

    user.books.append(book)
    db.session.add(user)
    db.session.commit()

    return jsonify(('msg', 'ok')), 200


"""@app.route("/library", methods=["GET"])
def library_get():

    user_id = request.form.get('id')
    user = User.query.get(1)
    library = User.books
    return book_schema.jsonify(library)"""
=======
>>>>>>> fe972578f02771f530e5ee3b7b1a3a1e18f00a2e
