from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import *

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


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


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
            }

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
