from flask import request, jsonify, redirect, render_template
from werkzeug.security import generate_password_hash

from app.models import *
from api import app


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


@app.route("/user", methods=["GET"])
# Get all books
def user_get():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    response = jsonify(result.data)
    response.status_code = 200
    return response


@app.route("/users", methods=['POST'])
def user_add(username, password, firstName, lastName, phone, email):

    hashedpassword = generate_password_hash(password)

    new_user = User(username, hashedpassword, firstName, lastName, phone, email)
    db.session.add(new_user)
    db.session.commit()
