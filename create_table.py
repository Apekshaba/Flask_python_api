import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS Inventory(name text,category text, expiry_date INTEGER, quantity real, manufacturing_date INTEGER,id INTEGER PRIMARY KEY, image BLOB NOT NULL, status text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(name text, price real)"
cursor.execute(create_table)      # make sure to delete this table before pushing it into the repository


connection.commit()

connection.close()
