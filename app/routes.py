from flask import render_template

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
