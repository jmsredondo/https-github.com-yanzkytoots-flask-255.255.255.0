import requests
from flask import render_template, request, redirect

from app import app
from forms import RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template('index.html')


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
            "password": form.username.data,
            "firstName": form.username.data,
            "lastName": form.username.data,
            "phone": form.username.data,
            "email": form.username.data,
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
    return render_template('Admin/user.html')


@app.route('/genre', methods=['GET'])
def genre():
    r = requests.get("http://localhost:80/genre")
    return render_template('Admin/genre.html', genre=r)


@app.route('/book', methods=['GET'])
def book():
    return render_template('Admin/book.html')


@app.route('/addgenre', methods=['GET'])
def addgenre():
    return render_template('Admin/addgenre.html')


@app.route('/addbook', methods=['GET'])
def addbook():
    return render_template('Admin/addbook.html')
