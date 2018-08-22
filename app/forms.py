from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('sign in')


class RegistrationForm(FlaskForm):
    username = StringField('username')
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    email = StringField('email address')
    password = PasswordField('new password')
    phone = StringField('phone')
    confirm = PasswordField('repeat password')

    submit = SubmitField('Create')


class AddBookForm(FlaskForm):
    bookname = StringField('book_name', validators=[DataRequired()])
    authorname = StringField('author', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('book_add')


class AddGenreForm(FlaskForm):
    typename = StringField('type', validators=[DataRequired()])
    genreid = StringField('genre', validators=[DataRequired()])
    submit = SubmitField('genre_add')
