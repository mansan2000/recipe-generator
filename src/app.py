import os
from aifc import Error

from models.models import Recipe, db, User
from flask import Flask, render_template, request, redirect, url_for, session, jsonify #Added jsonify 7/31, don't know how to check version to add to txt -B
from flask_session import Session
import sqlite3
from utils.helper_funcs import validate_password, get_saved_recipes_from_database

from flask_migrate import Migrate

from utils.openAIApi import get_recipe, recipeSelectionwant, recipeSelectionhave
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
app.config['SECRET_KEY'] = '1029384756'
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


@app.route('/logout')
def logout():
    # Clear the session when the user logs out
    session.clear()
    return redirect(url_for('login'))


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
            session['user'] = username
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
        selected_allergies = request.form.getlist('allergies')
        allergies = ', '.join(selected_allergies)

        print("Selected allergies:", selected_allergies)

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

@app.route('/generate-recipes-want', methods=['POST'])
def generate_recipes_want():
    data = request.json
    wanted = data.get('wanted')
    ranOut = data.get('ranOut')
    allRows = User.query.all()
    allergies = ""  # TODO: Change to get from database
    for user in allRows:
        if user.username == session['user']:
            allergies = user.allergies


    recipe_data = recipeSelectionwant(wanted, ranOut, allergies)
    recipes = get_recipe(recipe_data)

    session['generated_recipes'] = recipes

    return jsonify({'success': True})

@app.route('/generate-recipes-have', methods=['POST'])
def generate_recipes_have():
    data = request.json
    have = data.get('have')
    allergies = " I am allergic to nuts."  # TODO: Change to get from database

    recipe_data = recipeSelectionhave(have, allergies)
    recipes = get_recipe(recipe_data)

    session['generated_recipes'] = recipes

    return jsonify({'success': True})

@app.route('/results')
def view_results():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Get the generated recipes from the session
    recipes = session.get('generated_recipes')
    # Remove the recipes from the session to avoid showing them on the next visit
    # session.pop('generated_recipes', None)

    if recipes is not None:
        print("there are recipes")
        print(recipes)
        return render_template("/account/results.html", recipes=recipes)
    return render_template("/account/results.html")


@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({"message": "Invalid Content-Type"}), 415

    data = request.get_json()
    title = data.get('title')
    ingredients = data.get('ingredients')

    new_recipe = Recipe(session['user'], title, ingredients)
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({"message": "Recipe saved successfully!"})


@app.route("/saved-recipes")
def saved_recipes():
    recipes = get_saved_recipes_from_database(session['user'])
    saved_recipes_data = get_recipe(recipes)

    return render_template("/account/saved_recipes.html", saved_recipes_data = saved_recipes_data)

if __name__ == '__main__':
    app.run()
