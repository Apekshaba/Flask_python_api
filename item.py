from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from datetime import datetime


class Item(Resource):
    TABLE_NAME = 'Inventory'

    parser = reqparse.RequestParser()
    parser.add_argument('category',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('expiry_date',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('quantity',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('manufacturing_date',
        type=int,
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
            return item
        return {'message': 'Item not found'}, 404


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {
                        'name': row[0],
                        'category': row[1],
                        'expiry_date': row[2],
                        'quantity': row[3],
                        'manufacturing_date': row[4],
                        'id': row[5],
                        'image': row[6]
                    }
            }


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
            'image': data['image']
        }

        try:
            Item.insert(item)

        except:
            return {"message": "An error occurred inserting the item."}

        return {"message": "Inserted successfully."}, 200

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['name'], item['category'],item['expiry_date'], item['quantity'], item['manufacturing_date'], item['id'], item['image'], item['status']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET status=TRUE WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

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

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET quantity=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['quantity'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    TABLE_NAME = 'Inventory'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'category': row[1],'expiry_date': row[2], 'quantity': row[3], 'manufacturing_date': row[4], 'id': row[5], 'image': row[6], 'status': row[7]})
        connection.close()

        return {'items': items}
