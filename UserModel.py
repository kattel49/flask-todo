from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import relationship
from db import BASE, SALT, engine
import bcrypt
from ListModel import Lists

class Users(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password_hash = Column(String(128))
    children = relationship(Lists, cascade="all, delete")

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password_hash = self.hash_password(password)
    
    def hash_password(self, password: str) -> str:
        print(password.encode("utf8"))
        return bcrypt.hashpw(password.encode("utf8"), SALT).decode("utf8")
    
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), self.password_hash.encode("utf8"))

if __name__ == "__main__":
    if not inspect(engine).has_table("users"):
        BASE.metadata.create_all(engine)