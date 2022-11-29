from flask import Flask
from flask_restful import Api

from dotenv import load_dotenv
import os

from RegistrationResource import Registration
from LoginResource import Login
from ListResource import List
from ItemResource import Item

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

app = Flask(__name__)
api = Api(app)

api.add_resource(Registration, "/register")
api.add_resource(Login, "/login")
api.add_resource(List, "/lists")
api.add_resource(Item, "/items/<string:list_id>")

if __name__ == "__main__":
    app.run(debug=True)