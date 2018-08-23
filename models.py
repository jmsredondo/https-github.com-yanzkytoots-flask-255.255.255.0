from app import db, ma
from passlib.hash import pbkdf2_sha256 as sha256


# MODELS #
class User(db.Model):
    __tablename__ = 'users'

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

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def get_all(cls):
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return result

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def detail(cls, id):
        user = User.query.filter_by(id=id).first()
        result = user_schema.jsonify(user)
        return result

    @classmethod
    def delete(cls, id):
        try:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            result = user_schema.jsonify(user)
            return result
        except:
            return {'message': 'Something went wrong'}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def add_book_to_library(self, book_id, user_id):
        user = User.query.get(user_id)
        book = Book.query.get(book_id)
        user.books.append(book)

        db.session.add(user)
        db.session.commit()

    @classmethod
    def get_library(self, user_id):
        user = User.query.get(user_id)

        all_books = user.books
        result = books_schema.jsonify(all_books)
        return result


class RevokedTokenModel(db.Model):

    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_book_name(cls, book_name):
        return cls.query.filter_by(book_name=book_name).first()

    @classmethod
    def find_by_author(cls, author):
        return cls.query.filter_by(author=author).first()

    @classmethod
    def detail(cls, id):
        book = Book.query.filter_by(id=id).first()
        result = book_schema.jsonify(book)
        return result

    @classmethod
    def delete(cls, id):
        #try:
            book = Book.query.get(id)
            db.session.delete(book)
            db.session.commit()
            result = book_schema.jsonify(book)
            return result
        #except:
            #return {'message': 'Something went wrong'}

    @classmethod
    def get_all(cls):
        all_books = Book.query.all()
        result = books_schema.dump(all_books)
        return result

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(self, new_book, id):
        db_book = Book.query.get(id)
        db_book.book_name = new_book.book_name
        db_book.author = new_book.author
        db_book.description = new_book.description
        db.session.add(db_book)
        db.session.commit()


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

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, genre):
        return cls.query.filter_by(genre=genre).first()

    @classmethod
    def find_by_type(cls, type):
        return cls.query.filter_by(type=type).first()

    @classmethod
    def find_by_book(cls, id):
        pass

    @classmethod
    def update(self, new_genre, id):
        db_genre = Genre.query.get(id)
        db_genre.genre = new_genre.genre
        db_genre.type = new_genre.type
        db.session.add(db_genre)
        db.session.commit()

    @classmethod
    def detail(cls, id):
        genre = Genre.query.filter_by(id=id).first()
        result = genre_schema.jsonify(genre)
        return result

    @classmethod
    def delete(cls, id):
        try:
            genre = Genre.query.get(id)
            db.session.delete(genre)
            db.session.commit()
            result = genre_schema.jsonify(genre)
            return result
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def get_all(cls):
        all_genres = Genre.query.all()
        result = genres_schema.dump(all_genres)
        return result

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def add_book(self, book_id, id):
        genre = Genre.query.get(id)
        book = Book.query.get(book_id)

        genre.books.append(book)
        db.session.add(genre)
        db.session.commit()

    @classmethod
    def get_all_books(self, id):
        genre = Genre.query.get(id)

        all_books = genre.books
        result = books_schema.jsonify(all_books)
        return result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)


class Library(db.Model):
    __tablename__ = 'libraries'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=True)


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
