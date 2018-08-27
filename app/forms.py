from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('sign in')


class DeleteBook(FlaskForm):
    bookid = StringField('bookid', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
            validators.DataRequired(message='The name of the username is not empty.'),
            validators.Length(min=6, max=18, message='The user name must be more than% (min) D and less than% (max) d')
        ])
    firstname = StringField('Firstname', [validators.Length(min=1, max=50, message='The first name must be more than% (min) D and less than% (max) d')])
    lastname = StringField('Lastname', [validators.Length(min=1, max=50, message='The last name must be more than% (min) D and less than% (max) d')])
    email = StringField('Email Address', [validators.Length(min=6, max=60, message='The Email must be more than% (min) D and less than% (max) d')])
    phone = StringField('Phone')
    password = PasswordField('Password', validators=[
            validators.DataRequired(message='The password cannot be empty.'),
            validators.Length(min=8, message='The username length must be more than% (min) d'),
            validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
                              message='The password is at least 8 characters, at least 1 uppercase letters, 1 lowercase letters, 1 numbers and 1 special characters.')

        ])
    confirm = PasswordField('Repeat password')


class AddBookForm(FlaskForm):
    book_name = StringField('book_name', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddGenreForm(FlaskForm):
    genre = StringField('genre', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])
    submit = SubmitField('Add')
