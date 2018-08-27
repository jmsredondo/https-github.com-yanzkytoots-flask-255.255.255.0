import requests
from flask import render_template, request, redirect, json, session

from app import app
from forms import RegistrationForm, LoginForm, AddGenreForm, AddBookForm, DeleteBook


@app.route('/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            userdict = {
                "username": form.username.data,
                "password": form.password.data
            }

            r = requests.post("http://localhost:80/users/login", data=userdict)
            print r.status_code
            print r.content
            if r.status_code == 200:
                session['username'] = form.username.data
                return render_template('Admin/dashboard.html', username=form.username.data)
            return redirect('/#loginFailed')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')
