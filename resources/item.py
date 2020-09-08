from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from datetime import datetime
from models.item import ItemMode

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('category',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('expiry_date',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('quantity',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('manufacturing_date',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('image',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('status',
        type=bool,
        required=True,
        help="deleted status!"
    )


    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return expired(item)
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = {
            'name': name,
            'category': data['category'],
            'expiry_date': data['expiry_date'],
            'quantity': data['quantity'],
            'manufacturing_date': data['manufacturing_date'],
            'id': data['id'],
            'image': data['image'],
            'status': data['status']
        }

        try:
            Item.insert(item)

        except:
            return {"message": "An error occurred inserting the item."}

        return {"message": "Inserted successfully."}, 200

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'category': data['category'], 'quantity': data['quantity']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}
        return updated_item


class ItemList(Resource):
    TABLE_NAME = 'Inventory'

    def get(self):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
