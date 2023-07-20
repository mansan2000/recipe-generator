import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()
cur.execute("INSERT INTO recipes (user, recipe) VALUES (?, ?)",
            ('Emanuel', 'First Recipe')
            )





connection.commit()
connection.close()