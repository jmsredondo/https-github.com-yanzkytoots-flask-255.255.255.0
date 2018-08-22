import requests
from flask import jsonify, request, render_template, redirect, session, json
from werkzeug.security import generate_password_hash

from app.models import *
from app import app
from forms import RegistrationForm


@app.route('/testing', methods=['GET', 'POST'])
def testing():
    form = RegistrationForm()
    return render_template('register.html', form=form)

"""
def get_testing():
    form = RegistrationForm()
    new_dict = {
        'username': form.username,
        'password': form.password,
        'firstname': form.firstname,
        'lastname': form.lastname,
        'phone': form.phone,
        'email': form.email
    }
    print "Hello"
    print new_dict
    return new_dict


@app.route('/testing_res', methods=['GET'])
def res_testing():
    print "Hi"
    print get_testing()
"""
