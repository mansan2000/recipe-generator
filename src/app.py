import os
from aifc import Error

from models.models import Recipe, db, User
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import sqlite3
from utils.helper_funcs import validate_password

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

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '1029384756'  # Change this to a random secret key
Session(app)


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database/database.db')
        print("Connection to SQLite DB successful")
        return conn
    except Error as e:
        print(f"The error '{e}' occurred while connecting to the SQLite database")

    return conn


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/generate-recipes')
def generate():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("/account/generate.html")


@app.route('/view-recipes')
def view():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("/account/view.html")


@app.route('/login')
def login():
    return render_template('/login/login.html')


@app.route('/check-credentials', methods=['GET', 'POST'])
def checkCredentials():
    username = request.form.get('username')
    password = request.form.get('password')

    for user in User.query.all():
        print(user.password, user.username)
        print(username, password)
        if user.password == password and user.username == username:
            session['logged_in'] = True
            return render_template("/account/generate.html")
    return render_template("/login/login.html", incorrect="Invalid Credentials please try again")


@app.route('/signup', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        first = request.form.get('first')
        last = request.form.get('last')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        allergies = request.form.get('allergies')

        if confirm_password != password:
            return render_template("login/signup.html", error_type="match")

        requirements_met = validate_password(password)
        if not requirements_met:
            return render_template("login/signup.html", error_type="requirements")

        allRows = User.query.all()
        usernames = []
        for user in allRows:
            usernames.append(user.username)
        if username in usernames:
            return render_template("login/signup.html", error_type="unique")

        # new user added to database
        new_user = User(first, last, username, password, allergies)
        db.session.add(new_user)
        db.session.commit()

    return render_template('/login/signup.html')


if __name__ == '__main__':
    app.run()
