from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import *

login_parser = reqparse.RequestParser(bundle_errors=True)
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

reg_parser = reqparse.RequestParser(bundle_errors=True)
reg_parser.add_argument('username', help='This field cannot be blank', required=True)
reg_parser.add_argument('password', help='This field cannot be blank', required=True)
reg_parser.add_argument('firstName', help='This field cannot be blank', required=True)
reg_parser.add_argument('lastName', help='This field cannot be blank', required=True)
reg_parser.add_argument('phone', help='This field cannot be blank', required=True)
reg_parser.add_argument('email', help='This field cannot be blank', required=True)
reg_parser.add_argument('balance', help='This field cannot be blank', required=False)

id_parser = reqparse.RequestParser(bundle_errors=True)
id_parser.add_argument('book_id', help='This field cannot be blank', required=True)
id_parser.add_argument('user_id', help='This field cannot be blank', required=True)


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 400

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 400


class UserMethods(Resource):
    def get(self):
        return User.get_all()

    def delete(self):
        return User.delete_all()

    def post(self):
        data = reg_parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        elif User.find_by_email(data['email']):
            return {'message': 'User email {} already exists'.format(data['email'])}
        elif User.find_by_phone(data['phone']):
            return {'message': 'User phone {} already exists'.format(data['phone'])}

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            balance=data['balance'],
            phone=data['phone']
        )

        try:
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format(data['username'])
            }, 200

        except:
            return {'message': 'Something went wrong'}, 500


class UserDetailMethods(Resource):
    def get(self, pk):
        return User.detail(pk)

    def delete(self, pk):
        return User.delete(pk)


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class LibraryMethods(Resource):
    def post(self):
        data = id_parser.parse_args()
        """if Genre.find_by_book(data['book_id']):
            return {'message': 'Book being added already exists in this genre'}"""
        try:
            User.add_book_to_library(data['book_id'], data['user_id'])
            result = Book.detail(data['book_id'])
            result.content_status = 200
            return result
        except:
            return {
                'message': 'Authentication information is missing or invalid'
            }, 401


class LibraryDetailMethods(Resource):
    def get(self, pk):
        if User.find_by_id(pk):
            return User.get_library(pk)
        else:
            return {
                'message': 'User not found'
            }, 404