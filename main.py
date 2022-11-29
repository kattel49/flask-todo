from flask import Flask
from flask_restful import Api, Resource

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

app = Flask(__name__)
api = Api(app)



if __name__ == "__main__":
    app.run(debug=True)