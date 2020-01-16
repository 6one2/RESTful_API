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

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}


    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    # @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"The item {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

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
