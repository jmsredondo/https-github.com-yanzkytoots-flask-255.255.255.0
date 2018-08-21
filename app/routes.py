from flask import jsonify, request, render_template, redirect


from app import app
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


def __init__(self, username, password):
    self.username = username
    self.password = password


@app.route('/signin', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':

        user = User.query.all()
        for u in user:
            if u.username == username and check_password_hash(u.password, password):
                return render_template('Admin/dashboard.html', name=username)

        return redirect('/#loginFailed')
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')


@app.route('/users', methods=['GET'])
def users():
    return render_template('Admin/tables.html')


@app.route('/shookedbtn', methods=['GET'])
def shookedbtn():
    return render_template('Admin/index.html')


@app.route('/gen', methods=['GET'])
def gen():
    return render_template('Admin/gen.html')


@app.route('/libr', methods=['GET'])
def libr():
    return render_template('Admin/libr.html')


@app.route('/', methods=['GET'])
def inde():
    return render_template('Admin/index.html')


@app.route('/addgenre', methods=['GET'])
def addgenre():
    return render_template('Admin/addgenre.html')


@app.route('/addbook', methods=['GET'])
def addbook():
    return render_template('Admin/addbook.html')


@app.route('/boks', methods=['GET'])
def boks():
    return render_template('Admin/boks.html')


@app.route('/forgot', methods=['GET'])
def forgot():
    return render_template('forgot-password.html')


@app.route('/signup', methods=['POST', 'GET'])
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

    return render_template('register.html')


@app.route('/book', methods=['GET'])
def books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)

    return render_template('Admin/tables.html', ha=result)