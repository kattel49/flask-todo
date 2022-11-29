### Create a virtualenv
virtualenv venv

### Activate the virtualenv
source venv/bin/activate

### Install dependencies
pip3 install -r requirements.txt

### Create .env file
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=your_database
SALT=bcrypt.gensalt()
SECRET_KEY=randomstringtomakeitsecure

### Creation of Tables
python3 UserModel.py

### localhost:5000/register
{"username": "username", "password": "password"} => POST

### localhost:5000/login
{"username": "username", "password": "password"} => POST

### localhost:5000/lists
GET
POST => {"title": "List title"}
PUT => {"list_id": "list_id", "title": "Updated Title"}
DELETE => {"list_id": "list_id"}

### localhost:5000/items/<list_id>
GET
POST => {"body": "Body of the item"}
PUT => {"item_id": "item_id", "body": "Updated Body"}
DELETE => {"item_id": "item_id"}