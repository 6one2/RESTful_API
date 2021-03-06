from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = 'Every item needs a store id.'
    )

    # @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @fresh_jwt_required # requires a fresh access_token
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"The item {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500 # internal server error

        return item.json(), 201

    @fresh_jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required"}, 401

        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": f"The item {name} does not exists"}, 404

        item.delete_from_db()
        return {"message": f"Item {name} deleted"}, 200

    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {
            "items": items,
            "your id": user_id,
            }, 200

        return {
            'items': [item['name'] for item in items],
            'message': 'more data available if you log in'
        }, 200
