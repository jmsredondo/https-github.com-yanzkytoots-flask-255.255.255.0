import requests
from flask import render_template, request, redirect, json, session

from app import app
from forms import RegistrationForm, LoginForm, AddGenreForm, AddBookForm, DeleteBook


@app.route('/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            userdict = {
                "username": form.username.data,
                "password": form.password.data
            }

            r = requests.post("http://localhost:80/users/login", data=userdict)
            print r.status_code
            print r.content
            if r.status_code == 200:
                session['username'] = form.username.data
                return render_template('Admin/dashboard.html', username=form.username.data)
            return redirect('/#loginFailed')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
<<<<<<< HEAD
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

=======
    form = RegistrationForm()
    if form.validate_on_submit():
        reg = {
            "username": form.username.data,
            "password": form.password.data,
            "firstName": form.firstname.data,
            "lastName": form.lastname.data,
            "phone": form.phone.data,
            "email": form.email.data,
            "balance": 0
        }

        r = requests.post("http://localhost:80/users", data=reg)
        print r.status_code
        print r.content
        if r.status_code == 200:
            return redirect('/#success')
    return render_template('register.html', form=form)


@app.route('/delbook/<id>', methods=['POST'])
def delbook(id):
    print id
    r = requests.delete("http://localhost:80/book/" + id)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/addbook', methods=['POST'])
def addbook():
    a = request.form
    print a['description']
    print id
    r = requests.post("http://localhost:80/book", json=a)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)
>>>>>>> ec52115d1bb294a7c1ede3a67d7da21600fe6fd8


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')


@app.route('/book', methods=['GET', 'POST'])
def book():
    r = requests.get("http://localhost:80/book")
    result = json.loads(r.content)
    return render_template('Admin/books.html', books=result)


@app.route('/bookaddsuccess', methods=['GET', 'POST'])
def bookaddsuccess():
    return redirect('/book#bookadd')


@app.route('/bookdelsuccess', methods=['GET', 'POST'])
def bookdelsuccess():
    return redirect('/book#bookdelete')


@app.route('/user', methods=['GET'])
def user():
    r = requests.get("http://localhost:80/users")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/user.html', users=result)


@app.route('/deluser/<id>', methods=['POST'])
def deluser(id):
    print id
    r = requests.delete("http://localhost:80/users/" + id)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/userdelsuccess', methods=['GET'])
def delusersuccess(id):
    return redirect('/user#userdelete')


@app.route('/delgenre/<id>', methods=['POST'])
def delgenre(id):
    print id
    r = requests.delete("http://localhost:80/genre/" + id)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/genredelsuccess', methods=['GET', 'POST'])
def genredelsuccess():
    return redirect('/genre#genredelete')


@app.route('/genreaddsuccess', methods=['GET', 'POST'])
def genreaddsuccess():
    return redirect('/genre#genreadd')


@app.route('/genre', methods=['GET', 'POST'])
def genre():
    r = requests.get("http://localhost:80/genre")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/genre.html', genres=result)


<<<<<<< HEAD
    user_id = request.form.get('id')
    user = User.query.get(1)
    library = User.books
    return book_schema.jsonify(library)"""

=======
@app.route('/addgenre', methods=['POST'])
def addgenre():
    a = request.form
    r = requests.post("http://localhost:80/genre", json=a)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)
>>>>>>> ec52115d1bb294a7c1ede3a67d7da21600fe6fd8
