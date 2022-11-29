from dotenv import load_dotenv
import os
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def decode_token(token):
    try:
        if token is None:
            return None
        tmp = token.split(" ")[1]
        return jwt.decode(tmp, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return None