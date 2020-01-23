from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'gdjqoiuj7Gh'
api = Api(app)

# create the database if it does not exists (no need for create_tables.py anymore)
# still need to run app.py from /code folder
@app.before_first_request
def create_tables():
    db.create_all()

#security protocol for authentication of users
jwt = JWT(app, authenticate, identity) # create endpoint /auth

# create the endpoints link to ressources
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__': # in case we were to import app.py -> do not run
    db.init_app(app)
    app.run(port = 5000, debug=True)
