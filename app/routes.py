import requests
from flask import render_template, request, redirect, json, session, jsonify

from app import app, photos
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

    r = requests.post("http://localhost:80/genre/addbook/" + genreid, json={'book_id': bookid})
    print r.status_code
    return str(r.status_code)


@app.route('/addBookToGenre', methods=['GET'])
def addBookToGenre():
    reg = {
        "book_id": request.form('')
    }
    r = requests.post("http://localhost:80/genre/addbook/", data=reg)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return redirect('/book')

    return redirect('/book')


@app.route('/sess', methods=['GET'])
def asda():
    print session['admin']

    return "wahha"


@app.route('/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if 'admin' in session:
        print "yeh"
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

                if form.username.data == 'admin':

                    return render_template('Admin/dashboard.html', username=form.username.data, sess=form.username.data)
                else:
                    return render_template('Admin/dashboard.html', username=form.username.data)
            return redirect('/#loginFailed')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')


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
    a = request.form
    print a['description']
    print id
    r = requests.post("http://localhost:80/book", json=a)
    print r.status_code
    print r.content
    if r.status_code == 200:
        return str(r.status_code)
    return str(r.status_code)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('Admin/dashboard.html')


@app.route('/book', methods=['GET', 'POST'])
def book():
    r = requests.get("http://localhost:80/book")
    result = json.loads(r.content)
    return render_template('Admin/books.html', books=result)


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
    print id
    r = requests.delete("http://localhost:80/users/" + id)
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
    print id
    r = requests.delete("http://localhost:80/genre/" + id)
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
    r = requests.get("http://localhost:80/genre")
    print r.content
    result = json.loads(r.content)
    return render_template('Admin/genre.html', genres=result)


@app.route('/addgenre', methods=['POST'])
def addgenre():
    a = request.form
    r = requests.post("http://localhost:80/genre", json=a)
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
