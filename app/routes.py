import requests
from flask import jsonify, request, render_template, redirect, session, json
from werkzeug.security import generate_password_hash

from api.users import user_add
from app.models import *
from app import app


@app.route('/signin', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.all()
        for u in user:
            if u.username == username and u.password == password:
                session['user'] = username
                return redirect('/dashboard')
        return redirect('/#loginFailed')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        user_add(username, password, firstname, lastname, phone, email)

        return redirect('/#success')

    return render_template('registration.html')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template('Admin/dashboard.html')


@app.route('/user', methods=['GET'])
def users():
    all_users = requests.get('http://localhost:80/user').content
    result = json.loads(all_users)
    return render_template('Admin/user.html', users=result)


@app.route('/book', methods=['GET'])
def book():
    all_books = requests.get('http://localhost:80/book').content
    result = json.loads(all_books)
    return render_template('Admin/book.html', books=result)


@app.route('/', methods=['GET'])
def logout():
    return render_template('Admin/index.html')


@app.route('/shookedbtn', methods=['GET'])
def shookedbtn():
    return render_template('Admin/dashboard.html')


@app.route('/genre', methods=['GET'])
def genre_get():
    all_genres = requests.get('http://localhost:80/genre').content
    result = json.loads(all_genres)
    return render_template('Admin/genre.html', genres=result)


@app.route('/library', methods=['GET'])
def libr():
    return render_template('Admin/libr.html')


@app.route('/forgot', methods=['GET'])
def landing():
    return render_template('forgot-password.html')



