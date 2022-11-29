from sqlalchemy import ForeignKey, Column, Integer, String, inspect
from db import BASE, engine

class Items(BASE):
    __tablename__="items"
    
    id = Column(Integer, primary_key=True)
    body = Column(String(64))
    list_id = Column(Integer, ForeignKey("lists.id"))