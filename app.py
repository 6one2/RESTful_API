import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # read the value of DATABASE_URL in the environment defined, otherwize default value 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #database for local test
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # enable log from Flask

app.secret_key = 'gdjqoiuj7Gh'
api = Api(app)

# need to work locally? in run.py for server deployment
@app.before_first_request
def create_tables():
    db.create_all()

#security protocol for authentication of users
jwt = JWT(app, authenticate, identity) # create endpoint /auth

# create the endpoints link to ressources
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__': # in case we were to import app.py -> do not run
    db.init_app(app)
    app.run(port = 5000, debug=True)
