import requests
from flask import render_template, request, redirect, session

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
        print userdict
        r = requests.post("http://localhost:80/users/login", data=userdict)
        print r.status_code
        if r.status_code == 200:
            return render_template('Admin/dashboard.html', username=form.username.data)
        return redirect('/login#loginFailed')
    return render_template('login.html', form=form)
