import requests

from app.forms import LoginForm


def login():
    form = LoginForm()
    userdict = {
        "username": form.username,
        "password": form.password
    }
    r = requests.post("http://localhost:9101/users/login", data=userdict)