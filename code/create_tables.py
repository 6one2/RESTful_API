import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create table with auto incrementing id -> INTEGER PRIMARY KEY for auto increment
# no need for id when we add user anymore!
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()
