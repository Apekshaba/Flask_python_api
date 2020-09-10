import unittest
import requests
import app
from resources.item import Item, ItemList

class Test_assignment(unittest.TestCase):

    def test_get(self):
        data = Item.get(can)
        self.assertEquals(data['name'], 'can')
        self.assertEquals(data['category'], 'softdrink')
        self.assertEquals(data['quantity'], 100)


    def test_delete(self):
        data = Item.delete(can)
        self.assertEquals(data.status_code, 200)


    def test_put(self):
        data = Item.put(can)
        self.assertEquals(data['name'], 'can')
        self.assertEquals(data['category'], 'softdrink')
        self.assertEquals(data['quantity'], '105')


    def test_get_items():
        data = ItemList.get()
        self.assertEquals(data.status_code, 200)

if __name__ == "__main__":
    unittest.main()
