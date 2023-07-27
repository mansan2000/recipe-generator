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
    first = db.Column(db.Text)
    last = db.Column(db.Text)
    password = db.Column(db.Text)
    username = db.Column(db.Text)
    recipe = db.Column(db.Text)
    prompt = db.Column(db.Text)

    def __init__(self, username, first, last, password, recipe, prompt):
        self.username = username
        self.first = first
        self.last = last
        self.password = password
        self.recipe = recipe
        self.prompt = prompt

    def __repr__(self):
        return f"User {self.username} recipe {self.recipe}"
