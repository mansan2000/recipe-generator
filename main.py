import sqlite3
from aifc import Error

from flask import Flask, render_template, request
import sqlite3
import openAIApi
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the SQLite database")

    return conn


@app.route('/process', methods=['POST'])
def process():
    user = request.form['user']
    instructions = request.form['instructions']
    recipe = openAIApi.get_recipe(instructions)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert the user and recipe into the recipes table
    cursor.execute('''
        INSERT INTO recipes (user, recipe) VALUES (?, ?)
    ''', (user, recipe))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return 'Data inserted successfully.'


if __name__ == '__main__':
    app.run()
