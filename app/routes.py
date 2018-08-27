import random

import requests
from app import app, photos
from flask import render_template, request, redirect, json, session, jsonify

from forms import RegistrationForm, LoginForm


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photos.save(request.files['photo'])
        return None
    return render_template('upload.html')


@app.route('/uploadpic/<id>/', methods=['GET', 'POST'])
def uploadpic(id):
    r = requests.get("http://localhost:80/book/" + id)
    print r.status_code
    print r.content

    return render_template('upload.html', id=id, data=r.content)


@app.route('/getGenre', methods=['GET'])
def getGenre():
    r = requests.get("http://localhost:80/genre")
    print r.status_code
    result = r.json()
    return jsonify(result)


@app.route('/addGenreToBook/<genreid>/<bookid>', methods=['GET'])
def addGenreToBook2(genreid, bookid):
    print genreid, bookid
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    r = requests.post("http://localhost:80/genre/addbook/" + genreid, json={'book_id': bookid}, headers=headers)
    print r.status_code
    return str(r.status_code)


@app.route('/addBookToGenre', methods=['GET'])
def addBookToGenre():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    reg = {
        "book_id": request.form('')
    }
    r = requests.post("http://localhost:80/genre/addbook/", data=reg, headers=headers)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return redirect('/book')

    return redirect('/book')


@app.route('/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if 'username' in session:
        print session['username']
        if session['username'] == 'admin':
            return render_template('Admin/dashboard.html', username=session['username'])
        return render_template('User/userdashboard.html', username=session['username'])
    if request.method == 'POST':
        if form.validate_on_submit():
            userdict = {
                "username": form.username.data,
                "password": form.password.data
            }
            r = requests.post("http://localhost:80/users/login", data=userdict)

            if r.status_code == 200:
                session['username'] = form.username.data
                result = json.loads(r.content)
                token = result['access_token']
                session['access_token'] = token

                if form.username.data == 'admin':
                    return render_template('Admin/dashboard.html', username=form.username.data)
                else:
                    return render_template('User/userdashboard.html', username=form.username.data)
            return redirect('/#loginFailed')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    headers = {'Authorization': 'Bearer '+session['access_token']}
    r = requests.post("http://localhost:80/users/logout", headers=headers)
    session.clear()
    print r.status_code
    print r.content
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        reg = {
            "username": form.username.data,
            "password": form.password.data,
            "firstName": form.firstname.data,
            "lastName": form.lastname.data,
            "phone": form.phone.data,
            "email": form.email.data,
            "balance": 0
        }

        r = requests.post("http://localhost:80/users", data=reg)
        print r.status_code
        print r.content
        if r.status_code == 200:
            return redirect('/#success')
    return render_template('register.html', form=form)


@app.route('/delbook/<id>', methods=['POST'])
def delbook(id):
    print id
    r = requests.delete("http://localhost:80/book/" + id)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/addbook', methods=['POST'])
def addbook():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    a = request.form
    print a['description']
    print id
    r = requests.post("http://localhost:80/book", json=a, headers=headers)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return render_template('login.html')
    if 'username' in session:
        if session['username'] == 'admin':
            return render_template('Admin/dashboard.html', username=session['username'])
        return render_template('login.html', username=session['username'])
    return render_template('login.html')


@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' in session:
        if session['username'] == 'admin':
            r = requests.get("http://localhost:80/book")
            result = json.loads(r.content)
            return render_template('Admin/books.html', books=result)
        return render_template('login.html')
    return render_template('login.html')


@app.route('/bookaddsuccess', methods=['GET', 'POST'])
def bookaddsuccess():
    return redirect('/book#bookadd')


@app.route('/bookdelsuccess', methods=['GET', 'POST'])
def bookdelsuccess():
    return redirect('/book#bookdelete')


@app.route('/user', methods=['GET'])
def user():
    r = requests.get("http://localhost:80/users")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/user.html', users=result)


@app.route('/deluser/<id>', methods=['POST'])
def deluser(id):
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    print id
    r = requests.delete("http://localhost:80/users/" + id, headers=headers)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/userdelsuccess', methods=['GET'])
def delusersuccess(id):
    return redirect('/user#userdelete')


@app.route('/delgenre/<id>', methods=['POST'])
def delgenre(id):
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    print id
    r = requests.delete("http://localhost:80/genre/" + id, headers=headers)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/genredelsuccess', methods=['GET', 'POST'])
def genredelsuccess():
    return redirect('/genre#genredelete')


@app.route('/genreaddsuccess', methods=['GET', 'POST'])
def genreaddsuccess():
    return redirect('/genre#genreadd')


@app.route('/genre', methods=['GET', 'POST'])
def genre():
    if 'username' in session:
        if session['username'] == 'admin':
            r = requests.get("http://localhost:80/genre")
            result = json.loads(r.content)
            return render_template('Admin/genre.html', genres=result)
        return render_template('login.html')
    return render_template('login.html')


@app.route('/addgenre', methods=['POST'])
def addgenre():
    headers = {'Authorization': 'Bearer ' + session['access_token']}
    a = request.form
    r = requests.post("http://localhost:80/genre", json=a, headers=headers)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/userdash', methods=['GET'])
def userdash():
    return render_template('User/userdashboard.html')


@app.route('/userbook', methods=['GET'])
def userbook():
    r = requests.get("http://localhost:80/book")
    result = json.loads(r.content)
    return render_template('User/userbooklist.html', books=result)


@app.route('/usergenre', methods=['GET'])
def usergenre():
    r = requests.get("http://localhost:80/genre")
    print r.content
    result = json.loads(r.content)
    return render_template('User/usergenrelist.html', genres=result)


@app.route('/userlibrary', methods=['GET'])
def userlibrary():
    return render_template('User/userlibrary.html')


@app.route('/userlanding', methods=['GET'])
def userlanding():
    return render_template('User/userlanding.html')
