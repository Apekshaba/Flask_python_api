import sqlite3
from flask_restful import Resource, reqparse

from models.user import User


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = {
            "username": data['username'],
            "password": data['password']
        }

        try:
            UserRegister.insert_user(user)
        except:
            return {"message": "User created successfully."}, 201