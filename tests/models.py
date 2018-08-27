from app import db


# ------------------------------ MODELS ------------------------------ #
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    firstName = db.Column(db.String(300), nullable=False)
    lastName = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String(300), nullable=False, unique=True)
    balance = db.Column(db.Integer, default=0)
    books = db.relationship('Book', secondary='libraries', lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def __init__(self, username, password, firstName, lastName, phone, email, balance):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.email = email
        self.balance = balance


class RevokedTokenModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(100))
    ratings = db.relationship('Rating', lazy='select',
                              backref=db.backref('books', lazy='joined'))

    def __init__(self, book_name, author, description):
        self.book_name = book_name
        self.author = author
        self.description = description


class Genre(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120))
    books = db.relationship('Book', secondary='categories', lazy='subquery',
                            backref=db.backref('genres', lazy=True))

    def __init__(self, genre, type):
        self.genre = genre
        self.type = type


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))


class Library(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Rating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=True)
