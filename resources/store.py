from flask_restful import Resource
from models.store import StoreModel
from flask_jwt_extended import jwt_required, fresh_jwt_required


class Store(Resource):
    @jwt_required
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    @fresh_jwt_required
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name '{name}' already exists."}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store"}, 500

        return store.json(), 201

    @fresh_jwt_required
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": f"Store {name} deleted"}


class StoreList(Resource):
    @jwt_required
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
        # change query.all() to own find_all() class method to avoid interaction with database in ressources

        # return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}
