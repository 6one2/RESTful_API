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
        return {'error': f'No item {name} was found'} 

    def post(self, name):
        item = {'name': name, 'price': 12.00}
        items.append(item)
        return item

api.add_resource(Item, '/item/<string:name>')

app.run(port = 5000)
