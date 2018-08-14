from app import db, ma


# MODELS #

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


# SCHEMAS #

class BookSchema(ma.Schema):
    class Meta:
        fields = ('book_name', 'author', 'description')


book_schema = BookSchema()
books_schema = BookSchema(many=True)