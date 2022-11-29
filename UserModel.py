from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import BASE, SALT
import bcrypt
from ListModel import Lists

class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password_hash = Column(String(128), unique=True)
    children = relationship("Lists", cascade="all, delete")

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password_hash = self.hash_password(password)
    
    def hash_password(self, password: str) -> None:
        return bcrypt.hashpw(password.encode("utf8"), SALT).decode("utf8")
    
    def check_password(self, password: str) -> None:
        return bcrypt.checkpw(password.encode("utf8"), self.password_hash.encode("utf8"))