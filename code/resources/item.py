import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'
    )

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"The item {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occured inserting the item"}, 500 # internal server error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        if not ItemModel.find_by_name(name):
            return {"message": f"The item {name} does not exists"}, 404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": f"Item {name} deleted"}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item:
            try:
                updated_item.update()
            except:
                return {"message": "An error occured inserting the item"}, 500 # internal server error

        else:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured inserting the item"}, 500 # internal server error

        return updated_item.json()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        row = result.fetchall()

        connection.close()

        return {"items": row}
