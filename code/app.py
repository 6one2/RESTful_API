from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'gdjqoiuj7Gh'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create endpoint /auth

# here we are not working with database but using python list.
items = []

#inheritance from the class Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x:x['name']==name, items), None)
        return {'item': item}, 200 if item else 404 # status codes (200:accepted, 404:not found)

    # @jwt_required()
    def post(self, name):
        if next(filter(lambda x:x['name']==name, items), None):
            return {'message': 'An item of name {name} already exists.'}, 400 # bad request

        request_data = Item.parser.parse_args()
        
        item = {'name': name,
                'price': request_data['price']}
        items.append(item)
        return item, 201 # status code for created

    # @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x:x['name']!=name, items))
        item = next(filter(lambda x:x['name']==name, items), None)
        if item:
            items.remove(item)
            return {'message': 'The item {name} has been deleted'}, 200

        return {'error': f"The item {name} does not exists"}, 404

    # @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args() # get only argument added to parser

        item = next(filter(lambda x:x['name']==name, items), None)
        if item is None:
            item = {'name': name,
                    'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item

class ItemList(Resource):
    def get(self):
        if items:
            return {'items': items}

        return {'error': f"No item created yet"}, 404

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug=True)
