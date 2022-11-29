from flask_restful import Resource, reqparse
from db import session
from UserModel import Users

reg_post = reqparse.RequestParser()
reg_post.add_argument("username", type=str, help="Username is required", required=True)
reg_post.add_argument("password", type=str, help="Password is required", required=True)

class Registration(Resource):
    def post(self):
        # parse fields
        reg_data = reg_post.parse_args()
        # check if the user already exists in the database
        db_user = session.query(Users).filter(Users.username==reg_data["username"]).first()
        if db_user is not None:
            return {"Err" : "Username already taken"}, 400
        # create new user
        new_user = Users(username=reg_data["username"], password=reg_data["password"])

        session.add(new_user)
        session.commit()
        #close the session
        user_name = new_user.username
        session.close()
        return {"data": {"username": user_name}}, 201