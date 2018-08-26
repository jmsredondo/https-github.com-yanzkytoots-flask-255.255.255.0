from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('sign in')


class DeleteBook(FlaskForm):
    bookid = StringField('bookid', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username')
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    email = StringField('Email Address')
    phone = StringField('Phone')
    confirm = PasswordField('Repeat password')
    password = PasswordField('Password')


class AddBookForm(FlaskForm):
    book_name = StringField('book_name', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddGenreForm(FlaskForm):
    genre = StringField('genre', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])
    submit = SubmitField('Add')
