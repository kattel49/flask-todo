from flask_restful import Resource, reqparse
from sqlalchemy import and_
from flask import request
from utils import decode_token
from ListModel import Lists
from db import session

list_parser = reqparse.RequestParser()
list_parser.add_argument("title", type=str, help="title is required")
list_parser.add_argument("list_id", type=int, help="ID of the list")

class List(Resource):
    def get(self):
        # decode token
        token = decode_token(request.headers.get("Authorization"))
        if token is None:
            return {"Err" : "Invalid Token"},400
        # get the user id from the decoded token
        user_id = token["user_id"]
        # get all lists from the database
        lists = [{"title": x.title, "list_id": x.id} for x in session.query(Lists).filter(Lists.user_id == user_id)]
        session.close()
        return {"data": {"lists": lists}}, 200

    def post(self):
        token = decode_token(request.headers.get("Authorization"))
        if token == None:
            return {"Err" : "Invalid Token"}, 400
        p_args = list_parser.parse_args()

        try:
            # create a new list
            new_list = Lists(title=p_args["title"], user_id=token["user_id"])
            session.add(new_list)
            # commit changes to the database
            session.commit()
            list_id = new_list.id
            session.close()
            return {"data": {"title": p_args["title"], "list_id": list_id}}, 200
        except:
            return {"Err": "Internal Error"}

    def delete(self):
        token = decode_token(request.headers.get("Authorization"))
        if token == None:
            return {"Err" : "Invalid Token"}, 400
        d_args = list_parser.parse_args()

        try:
            # fetch list from the database
            db_list = session.query(Lists).filter(and_(
                Lists.user_id==token["user_id"]),
                Lists.id == d_args["list_id"]
                ).first()
            title = db_list.title
            # delete list from the database
            session.delete(db_list)
            session.commit()
            session.close()
            return {"data": {"list_id": d_args["list_id"], "title": title}}, 200
        except:
            return {"Err": "Internal Error"}

    def put(self):
        token = decode_token(request.headers.get("Authorization"))
        if token == None:
            return {"Err" : "Invalid Token"}, 400
        p_args = list_parser.parse_args()

        try:
            # get the list
            db_list = session.query(Lists).filter(and_(
                Lists.user_id==token["user_id"]),
                Lists.id == p_args["list_id"]
                ).first()
            # update the title
            db_list.title = p_args["title"]
            session.add(db_list)
            # commit change
            session.commit()
            session.close()
            return {"data": {"list_id": p_args["list_id"], "title" : p_args["title"]}}, 200
        except:
            return {"Err": "Internal Error"}