from flask import Flask
from config import Config
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from resources import users_resource
import models


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(users_resource.UserMethods, '/users')
api.add_resource(users_resource.UserDetailMethods, '/users/<pk>')
api.add_resource(users_resource.UserLogin, '/users/login')
api.add_resource(users_resource.UserLogoutAccess, '/users/logout')

api.add_resource(users_resource.UserLogoutRefresh, '/users/logout/refresh')
api.add_resource(users_resource.TokenRefresh, '/token/refresh')
