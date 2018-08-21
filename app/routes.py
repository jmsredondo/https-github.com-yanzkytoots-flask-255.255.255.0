import requests
from flask import jsonify, request, render_template, redirect, session, json

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


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')


@app.route('/user', methods=['GET'])
def users():
    all_books = requests.get('http://localhost:80/book').content
    result = json.loads(all_books)
    return render_template('Admin/book.html', books=result)


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


@app.route('/book', methods=['GET'])
def boks():
    return render_template('Admin/book.html')
