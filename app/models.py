from app import db, ma


# MODELS #
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), index=True)
    password = db.Column(db.String(300), index=True)
    firstname = db.Column(db.String(300), index=True)
    lastname = db.Column(db.String(300), index=True)
    phone = db.Column(db.Integer, index=True)
    email = db.Column(db.String(300), index=True)

    def __init__(self, username, password, firstname, lastname, phone, email):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))

    # image
    # genre

    def __init__(self, book_name, author, description):
        self.book_name = book_name
        self.author = author
        self.description = description


class Genre(db.Model):

    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(300), unique=True, nullable=False)
    type = db.Column(db.String(120))

    def __init__(self, genre, type):
        self.genre = genre
        self.type = type

# SCHEMAS #


class BookSchema(ma.Schema):
    class Meta:
        fields = ('book_name', 'author', 'description')


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class GenreSchema(ma.Schema):
    class Meta:
        fields = ('genre', 'type')


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


class UserLogin(ma.Schema):
    class Meta:
        fields = ('username', 'password')


userAuth = UserLogin()

