from app import db, ma


# MODELS #
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    firstName = db.Column(db.String(300), nullable=False)
    lastName = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
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


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))

    # image

    def __init__(self, book_name, author, description):
        self.book_name = book_name
        self.author = author
        self.description = description


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120))
    books = db.relationship('Book', secondary='categories', lazy='subquery',
                            backref=db.backref('genres', lazy=True))

    def __init__(self, genre, type):
        self.genre = genre
        self.type = type


class Library(db.Model):
    __tablename__ = 'libraries'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# SCHEMA #
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_name', 'author', 'description')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'firstname', 'lastname', 'phone', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


class GenreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'genre', 'type')


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'firstName', 'lastName', 'phone', 'email', 'balance', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
