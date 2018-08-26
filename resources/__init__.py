from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)

jwt = JWTManager(app)

from resources import users_resource, books_resource, genres_resource
from app import models


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(users_resource.UserMethods, '/users')
api.add_resource(users_resource.UserDetailMethods, '/users/<pk>')
api.add_resource(users_resource.UserLogin, '/users/login')
api.add_resource(users_resource.UserLogout, '/users/logout')
# api.add_resource(users_resource.UserLogoutRefresh, '/users/logout/refresh')
# api.add_resource(users_resource.TokenRefresh, '/token/refresh')

api.add_resource(users_resource.LibraryMethods, '/library')
api.add_resource(users_resource.LibraryDetailMethods, '/library/<pk>')

api.add_resource(books_resource.BookMethods, '/book')
api.add_resource(books_resource.BookDetailMethods, '/book/<pk>')
api.add_resource(books_resource.BookRateMethods, '/rate')
api.add_resource(books_resource.BookRateDetailMethods, '/rate/<pk>')

api.add_resource(genres_resource.GenreMethods, '/genre')
api.add_resource(genres_resource.GenreDetailMethods, '/genre/<pk>')
api.add_resource(genres_resource.GenreBookMethods, '/genre/addbook/<pk>')
