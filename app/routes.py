from flask import jsonify, request, render_template, redirect, session
from app import app
from app import models
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET', 'POST'])
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

    return render_template('register.html')
