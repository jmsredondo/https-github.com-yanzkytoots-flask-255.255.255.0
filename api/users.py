from flask import request, jsonify, redirect, render_template
from werkzeug.security import generate_password_hash

from app.models import *
from api import app


@app.route("/user", methods=["GET"])
# Get all books
def user_get():
    all_users = User.query.all()
    result = books_schema.dump(all_users)
    response = jsonify(result.data)
    response.status_code = 200
    return response


@app.route("/users", methods=['POST'])
def user_add(username, password, firstName, lastName, phone, email):

    hashedpassword = generate_password_hash(password)

    new_user = User(username, hashedpassword, firstName, lastName, phone, email)
    db.session.add(new_user)
    db.session.commit()
