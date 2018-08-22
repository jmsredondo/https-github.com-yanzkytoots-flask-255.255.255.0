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
            "firstname": form.username.data,
            "lastname": form.username.data,
            "phone": form.username.data,
            "email": form.username.data,
            "balance":0
        }

        r = requests.post("http://localhost:80/users", data=reg)