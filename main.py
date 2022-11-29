from flask import Flask
from flask_restful import Api

from dotenv import load_dotenv
import os

from RegistrationResource import Registration

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

app = Flask(__name__)
api = Api(app)

api.add_resource(Registration, "/register")

if __name__ == "__main__":
    app.run(debug=True)