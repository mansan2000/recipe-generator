from aifc import Error

from flask import Flask, render_template, request
import sqlite3
import openAIApi
from database import insert_functions

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Hello World</h1>"


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database/database.db')
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the SQLite database")

    return conn


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user = data['user']
    instructions = data['instructions']
    recipe = openAIApi.get_recipe(instructions)
    print(recipe)

    insert_functions.insert_row(user, recipe)

    return 'Data inserted successfully.'


if __name__ == '__main__':
    app.run()
