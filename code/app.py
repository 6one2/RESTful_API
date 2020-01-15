from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = 'gdjqoiuj7Gh'
api = Api(app)

# here we are not working with database but using python list.
items = []

#inheritance from the class Resource
class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x:x['name']==name, items), None)
        return {'item': item}, 200 if item else 404 # status codes (200:accepted, 404:not found)

    def post(self, name):
        if next(filter(lambda x:x['name']==name, items), None):
            return {'message': 'An item of name {name} already exists.'}, 400 # bad request

        request_data = request.get_json()
        item = {'name': name,
                'price': request_data['price']}
        items.append(item)
        return item, 201 # status code for created

class ItemList(Resource):
    def get(self):
        if items:
            return {'items': items}

        return {'error': f"No item created yet"}, 404

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug=True)
