import os
from aifc import Error


from models.models import Recipe, db
from flask import Flask, render_template, request,  redirect, url_for
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


# @app.route('/')
# def login():
#     return render_template("login.html")




def check_user_credentials(username, password):
    user = Recipe.query.filter_by(username=username).first()
    return user is not None and user.password == password

def check_username(username):
    user = Recipe.query.filter_by(username=username).first()
    return user is not None

@app.route('/', endpoint='login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def process_form():
    username = request.form.get('username')
    password = request.form.get('password')

    if not check_username(username):
        return render_template('needtosignup.html')
    elif not check_user_credentials(username, password):
        return render_template('try_again.html')
    else:
        return render_template('secretpage.html')



def validate_password(password):
    upper = any(char.isupper() for char in password)
    lower = any(char.islower() for char in password)
    number = password[-1].isdigit()
    length = len(password) >= 8

    return upper and lower and number and length



@app.route('/signup.html', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        first = request.form.get('first')
        last = request.form.get('last')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

          # Check if passwords match
        if confirm_password != password:
            return render_template('try_again.html')

        # # Check if the password meets the requirements
        requirements_met = validate_password(password)
        if not requirements_met:
            return render_template('requirements.html')
        
        
        # new user added to database
        new_user = Recipe(first=first, last=last, username=username, password=password, recipe=None, prompt=None)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('thankyou'))

    return render_template('signup.html')



@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# @app.route('/process', methods=['POST'])
# def process():
#     user = request.form['user']
#     instructions = request.form['instructions']
#     recipe = get_recipe(instructions)
#     print(recipe)
#     insert_row(user, recipe, instructions)

#     return 'Data inserted successfully.'



if __name__ == '__main__':
    app.run()
