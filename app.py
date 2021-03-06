import os

from flask import Flask, jsonify, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import (UserRegister,
                    User,
                    UserLogin,
                    UserLogout,
                    TokenRefresh
                    )
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # read the value of DATABASE_URL in the environment defined, otherwize default value 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #database for local test
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True # enable log from Flask
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = 'gdjqoiuj7Gh' # app.config['JWT_SECRET_KEY']
api = Api(app)

# need to work locally? in run.py for server deployment
# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWTManager(app) # not create auth endpoint

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1: # instead of hard-coding, read from config file or database
        return {'is_admin': True}
    return {'is_admin': False}

## configuration / customization of error messages
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description':'the token has expired',
        'error':'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_loader(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    })

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


# create the endpoints link to ressources
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__': # in case we were to import app.py -> do not run
    db.init_app(app)
    app.run(port = 5000, debug=True)
