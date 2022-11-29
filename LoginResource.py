from flask_restful import Resource, reqparse
from UserModel import Users
from db import session
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

l_parse = reqparse.RequestParser()
l_parse.add_argument("username", type=str, help="Username required", required=True)
l_parse.add_argument("password", type=str, help="Password required", required=False)

class Login(Resource):
    def post(self):
        l_args = l_parse.parse_args()
        #fetch user from the database
        db_user = session.query(Users).filter(Users.username == l_args["username"]).first()
        if db_user is None:
            return {"Err": "Username/Password is invalid"}, 400
        if db_user.check_password(l_args["password"]):
            token = jwt.encode({"username": db_user.username, "user_id": db_user.id}, SECRET_KEY, algorithm="HS256")
            return {"data": {"token": token}}
        else:
            return {"Err": "Username/Password is invalid"}