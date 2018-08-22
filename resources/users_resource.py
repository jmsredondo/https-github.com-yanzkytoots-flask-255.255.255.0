from flask import session, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from werkzeug.security import check_password_hash

from app.models import *

# login_parser = reqparse.RequestParser()
# login_parser.add_argument('username', help='This field cannot be blank', required=True)
# login_parser.add_argument('password', help='This field cannot be blank', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)


reg_parser = reqparse.RequestParser()
reg_parser.add_argument('username', help='This field cannot be blank', required=True)
reg_parser.add_argument('password', help='This field cannot be blank', required=True)
reg_parser.add_argument('firstName', help='This field cannot be blank', required=True)
reg_parser.add_argument('lastName', help='This field cannot be blank', required=True)
reg_parser.add_argument('phone', help='This field cannot be blank', required=True)
reg_parser.add_argument('email', help='This field cannot be blank', required=True)
reg_parser.add_argument('balance', help='This field cannot be blank', required=False)


class UserRegistration(Resource):
    def post(self):
        data = reg_parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
            firstName=User.generate_hash(data['firstName']),
            lastName=User.generate_hash(data['lastName']),
            email=User.generate_hash(data['email']),
            balance=User.generate_hash(data['balance']),
            phone=User.generate_hash(data['phone']),

        )

        try:
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format(data['username'])
            }
        except:
            return {'message': 'Something went wrong'}, 500


class Log(Resource):
    def post(self):
        data = login_parser.parse_args()
        user = User.query.all()
        data = login_parser.parse_args()
        for u in user:
            if u.username == data['username'] and check_password_hash(u.password, data['password']):
                create_access_token(identity=data['username'])
                create_refresh_token(identity=data['username'])
                session['username'] = data['username']
                return "OK"


class UserLogin(Resource):
    def get(self):
        data = login_parser.parse_args()

        return data['password']

    def post(self):
        data = login_parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            session['user'] = data['username']
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'session': session
            }
        else:
            return {'message': 'Wrong credentials'}


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
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
