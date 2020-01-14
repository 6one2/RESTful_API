from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# here we are not working with database but using python list.
items = []

#inheritance from the class Resource
class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name']==name:
                return item

        return {'error': f"No item '{name}' was found"}, 404 # status code for not found

    def post(self, name):
        item = {'name': name, 'price': 12.00}
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
