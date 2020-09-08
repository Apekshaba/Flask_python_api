import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS Inventory(name text,category text, expiry_date string, quantity real, manufacturing_date string, id INTEGER PRIMARY KEY, image BLOB NOT NULL, status text, expired boolean)"
cursor.execute(create_table)


connection.commit()

connection.close()
