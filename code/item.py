import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"meassage": {"name": row[0], "price": row[1]}}
        return {"message": "Item not found"}, 404

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
