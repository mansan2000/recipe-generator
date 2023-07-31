import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/data.sqlite')
#
# db = SQLAlchemy(app)
# Migrate(app, db)
# from app import db

from database.database import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    recipe = db.Column(db.Text)
    prompt = db.Column(db.Text)

    def __init__(self, username, recipe, prompt):
        self.username = username
        self.recipe = recipe
        self.prompt = prompt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.Text)
    lastName = db.Column(db.Text)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    allergies = db.Column(db.Text)

    def __init__(self, firstName, lastName, username, password, allergies):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.password = password
        self.allergies = allergies

