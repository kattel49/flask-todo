from flask_restful import Resource, reqparse
from sqlalchemy import and_
from flask import request
from utils import decode_token
from ItemModel import Items
from ListModel import Lists
from db import session

item_parser = reqparse.RequestParser()
item_parser.add_argument("body", type=str)
item_parser.add_argument("item_id", type=int)

class Item(Resource):
    def get(self, list_id):

        # decode token
        token = decode_token(request.headers.get("Authorization"))
        if token is None:
            return {"Err" : "Invalid Token"},400
        # verify if the user owns the list
        verify_list = session.query(Lists).filter(Lists.id == list_id).first()
        if verify_list is None:
            return {"Err": "List does not exist"}, 400
        if verify_list.user_id == token["user_id"]:
            # get all items from the database
            items = [{"body": x.body, "item_id": x.id} for x in session.query(Items).filter(Items.list_id == list_id)]
            session.close()
            return {"data": {"items": items}}, 200
        else:
            return {"Err": "Unathorized Access"}, 400

    def post(self, list_id):
        token = decode_token(request.headers.get("Authorization"))
        if token == None:
            return {"Err" : "Invalid Token"}, 400
        p_args = item_parser.parse_args()

        try:
            verify_list = session.query(Lists).filter(Lists.id == list_id).first()
            if verify_list is None:
                return {"Err": "List does not exist"}, 400
            if verify_list.user_id == token["user_id"]:
                # create a new item
                new_item = Items(body=p_args["body"], list_id=list_id)
                session.add(new_item)
                # commit changes to the database
                session.commit()
                item_id = new_item.id
                session.close()
                return {"data": {"body": p_args["body"], "item_id": item_id}}, 200
            else:
                return {"Err": "Unathorized Access"}, 400
        except:
            return {"Err": "Internal Error"}, 500

    def delete(self, list_id):
        token = decode_token(request.headers.get("Authorization"))
        if token == None:
            return {"Err" : "Invalid Token"}, 400
        d_args = item_parser.parse_args()

        try:
            verify_list = session.query(Lists).filter(Lists.id == list_id).first()
            if verify_list is None:
                return {"Err": "List does not exist"}, 400
            if verify_list.user_id == token["user_id"]:
                # fetch item from the database
                db_item = session.query(Items).filter(and_(
                    Items.list_id == list_id,
                    Items.id == d_args["item_id"]
                    )).first()
                # check if the item exists
                if db_item is None:
                    session.close()
                    return {"Err": "Item does not exist"}
                body = db_item.body
                # delete list from the database
                session.delete(db_item)
                session.commit()
                session.close()
                return {"data": {"item_id": d_args["item_id"], "body": body}}, 200
            else:
                return {"Err": "Unathorized Access"}, 400
        except:
            return {"Err": "Internal Error"}, 500

    def put(self, list_id):
        token = decode_token(request.headers.get("Authorization"))
        if token == None:
            return {"Err" : "Invalid Token"}, 400
        p_args = item_parser.parse_args()
        try:
            verify_list = session.query(Lists).filter(Lists.id == list_id).first()
            if verify_list is None:
                return {"Err": "List does not exist"}, 400

            if verify_list.user_id == token["user_id"]:
                db_item = session.query(Items).filter(and_(
                        Items.id == p_args["item_id"],
                        Items.list_id == list_id
                    )).first()
                if db_item is None:
                    return {"Err": "Item does not exist"}
                db_item.body = p_args["body"]
                session.add(db_item)
                session.commit()
                session.close()
                return {"data": {"item_id": p_args["item_id"], "body": p_args["body"]}}, 200
            else:

                return {"Err": "Unathorized Access"}, 400
        except:
           return {"Err": "Internal Error"}, 500