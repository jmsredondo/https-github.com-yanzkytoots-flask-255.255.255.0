import requests
from flask import render_template, request, redirect, json

from app import app
from forms import RegistrationForm, LoginForm, AddGenreForm, AddBookForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/deluser', methods=['POST'])
def delusers():
    if request.method == 'POST':
        ayd = request.form.get('ayd')
        aydd = int(ayd)
        print type(aydd)
        d = {
            "book_id": ayd
        }
        r = requests.delete("http://localhost:80/book/<pk>", data=d)
        print r.content
        if r.status_code == 200:
            return redirect('/book#success')

    #elif request.method =='DELETE':

    return redirect('/book')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        userdict = {
            "username": form.username.data,
            "password": form.password.data
        }

        r = requests.post("http://localhost:80/users/login", data=userdict)
        if r.status_code == 200:
            return render_template('Admin/dashboard.html', username=form.username.data)
        return redirect('/login#loginFailed')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
        if r.status_code == 200:
            return redirect('/login#success')
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')


@app.route('/user', methods=['GET'])
def user():
    r = requests.get("http://localhost:80/users")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/user.html', users=result)


@app.route('/genre', methods=['GET'])
def genre():
    r = requests.get("http://localhost:80/genre")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/genre.html', genres=result)


@app.route('/addgenre', methods=['GET', 'POST'])
def genre_add():
    form = AddGenreForm()
    if form.validate_on_submit():
        reg = {
            "genre": form.genre.data,
            "type": form.type.data,

        }

        r = requests.post("http://localhost:80/genre", data=reg)
        print r.status_code
        if r.status_code == 200:
            return redirect('/genre')
    return render_template('Admin/addgenre.html', form=form)


@app.route('/book', methods=['GET'])
def book():
    r = requests.get("http://localhost:80/book")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/book.html', books=result)


@app.route('/addbook', methods=['GET', 'POST'])
def book_add():
    form = AddBookForm()
    if form.validate_on_submit():
        reg = {
            "book_name": form.book_name.data,
            "author": form.author.data,
            "description": form.description.data,

        }

        r = requests.post("http://localhost:80/book", data=reg)
        print r.status_code
        if r.status_code == 200:
            return redirect('/book')
    return render_template('Admin/addbook.html', form=form)
