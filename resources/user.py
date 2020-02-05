# import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type = str,
                            required = True,
                            help = 'This field cannot be left blank!'
                            )

_user_parser.add_argument('password',
                            type = str,
                            required = True,
                            help = 'You need to provide a password!'
                            )

class UserRegister(Resource):

    def post(cls):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": f"The user {data['username']} already exists"}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {"message": "An error occured inserting the user"}, 500 # internal server error
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        return {"message": "User created successfully."}, 201

class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200

class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200

        return {'message': 'Invalid credentials'}, 401
