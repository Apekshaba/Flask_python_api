from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from datetime import datetime
from resources.item import Item, ItemList


class ItemModel():
    TABLE_NAME = 'Inventory'


    @classmethod
    def expired(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        date = row[2]
        current_time = datetime.now()

        if date<=current_time:
            query = "UPDATE {table} SET expired=TRUE WHERE name=?".format(table=cls.TABLE_NAME)
            cursor.execute(query, (item['expired'], item['name']))
            return {'message':'product expired' }
        return item


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



    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['name'], item['category'],item['expiry_date'], item['quantity'], item['manufacturing_date'], item['id'], item['image'], item['status']))

        connection.commit()
        connection.close()


    @jwt_required()
    def delete_from_db(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET status=False WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()



    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET quantity=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['quantity'], item['name']))

        connection.commit()
        connection.close()
