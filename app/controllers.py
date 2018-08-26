import requests

from app.forms import LoginForm


def login():
    form = LoginForm()
    userdict = {
        "username": form.username,
        "password": form.password
    }
    r = requests.post("http://localhost:80/users/login", data=userdict)