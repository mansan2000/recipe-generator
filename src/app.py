import os
from aifc import Error

from flask import Flask, render_template, request
import sqlite3

from flask_migrate import Migrate

from utils.openAIApi import get_recipe
from utils.helper_funcs import insert_row


def create_app():
    flaskApp = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/data.sqlite')

    from database.database import db
    db.init_app(flaskApp)
    Migrate(flaskApp, db)

    return flaskApp


app = create_app()


@app.route('/')
def index():
    return render_template("index.html")


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
    user = request.form['user']
    instructions = request.form['instructions']
    recipe = get_recipe(instructions)
    print(recipe)
    insert_row(user, recipe, instructions)

    return 'Data inserted successfully.'


if __name__ == '__main__':
    app.run()
