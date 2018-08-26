from flask import session
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from app.models import *

# ------------------------------ PARSE INPUTS ------------------------------ #
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


# ------------------------------ ROUTE: /users/login ------------------------------ #
class UserLogin(Resource):
    # Login user and generate a token #
    def post(self):
        data = login_parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {
                       'message': 'Invalid credentials'
                   }, 400

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            # refresh_token = create_refresh_token(identity=data['username'])
            session['username'] = data['username']
            return {
                       'message': 'Logged in as {}'.format(current_user.username),
                       'access_token': access_token,




                       # 'refresh_token': refresh_token
                   }, 200
        else:
            return {
                       'message': 'Invalid credentials'
                   }, 400


# ------------------------------ ROUTE: /users/logout ------------------------------ #
class UserLogout(Resource):
    # Logout user and add access token to banlist #
    # @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                       'message': 'Access token has been revoked'
                   }, 200
        except:
            return {
                       'message': 'Something went wrong'
                   }, 400


"""
# ------------------------------ ROUTE: /users/logout/refresh ------------------------------ #
class UserLogoutRefresh(Resource):
	# Logout user and add refresh token to banlist #
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
            'message': 'Refresh token has been revoked'
            }, 200
        except:
            return {
            'message': 'Something went wrong'
            }, 400


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
"""


# ------------------------------ ROUTE: /users ------------------------------ #
class UserMethods(Resource):
    # Retrieve all users #
    def get(self):
        return User.get_all()

    # Delete all users #
    def delete(self):
        return User.delete_all()

    # Create a user #
    def post(self):
        data = reg_parser.parse_args()

        if User.find_by_username(data['username']):
            return {
                       'message': 'Username already exists in the database'
                   }, 202
        elif User.find_by_email(data['email']):
            return {
                       'message': 'User email already exists in the databse'
                   }, 202
        elif User.find_by_phone(data['phone']):
            return {
                       'message': 'User phone already exists in the database'
                   }, 202

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
                       'message': 'User successfully created'
                   }, 200

        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


# ------------------------------ ROUTE: /users/<pk> ------------------------------ #
class UserDetailMethods(Resource):
    # Retrieve a user #
    def get(self, pk):
        if User.find_by_id(pk):
            return User.detail(pk)
        else:
            return {
                       'message': 'User not found'
                   }, 404

    # Delete a user #
    def delete(self, pk):
        if User.find_by_id(pk):
            try:
                User.delete(pk)
                return {
                           'message': 'User successfully deleted'
                       }, 200
            except:
                return {
                           'message': 'Authentication information is missing or invalid'
                       }, 401
        else:
            return {
                       'message': 'User not found'
                   }, 404

    # Update an existing user's information
    def put(self, pk):
        data = reg_parser.parse_args()

        if not Genre.find_by_id(pk):
            return {
                       'message': 'User not found'
                   }, 404
        elif User.find_by_email(data['email']):
            return {
                       'message': 'User email already exists'
                   }, 202
        elif User.find_by_phone(data['phone']):
            return {
                       'message': 'User phone already exists'
                   }, 202

        new_user = User(
            username=User.username,
            password=User.generate_hash(data['password']),
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            balance=data['balance'],
            phone=data['phone']
        )

        try:
            User.update(new_user, pk)
            return {
                       'message': 'Successfully updated user information'
                   }, 200
        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


class LibraryMethods(Resource):
    # Add a book to user library #
    def post(self):
        data = id_parser.parse_args()
        if Library.find_by_user(data['user_id']) and Library.find_by_book(data['book_id']):
            return {
                       'message': 'Book already exists in user library'
                   }, 202
        try:
            User.add_book_to_library(data['book_id'], data['user_id'])
            return {
                       'message': 'Book successfully added to user library'
                   }, 200
        except:
            return {
                       'message': 'Authentication information is missing or invalid'
                   }, 401


class LibraryDetailMethods(Resource):
    # Retrieve all books in a user's library #
    def get(self, pk):
        if User.find_by_id(pk):
            return User.get_library(pk)
        else:
            return {
                       'message': 'User not found'
                   }, 404
