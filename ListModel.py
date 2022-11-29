from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import BASE
from ItemModel import Items


class Lists(BASE):
    __tablename__ = "lists"
    id = Column(Integer, primay_key=True)
    title = Column(String(64))
    user_id = Column(Integer, ForeignKey("users.id"))
    children = relationship("Items", cascade="all, delete")