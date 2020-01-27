import sqlite3
## make sure to run app.py and create_tables from same folder

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create table with auto incrementing id -> INTEGER PRIMARY KEY for auto increment
# no need for id when we add user anymore!
create_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users)

create_items = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_items)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")
connection.commit()
connection.close()
