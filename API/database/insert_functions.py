import sqlite3
import os


def insert_row(user, recipe):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    db_file = os.path.join(current_dir, 'database.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert the user and recipe into the recipes table
    cursor.execute('''
        INSERT INTO recipes (user, recipe) VALUES (?, ?)
    ''', (user, recipe))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
