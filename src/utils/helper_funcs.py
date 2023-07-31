from models.models import Recipe
from database.database import db


def insert_row(user, recipe, instructions):
    newRow = Recipe(user, recipe, instructions)
    db.session.add(newRow)
    db.session.commit()


def validate_password(password):
    upper = any(char.isupper() for char in password)
    lower = any(char.islower() for char in password)
    number = password[-1].isdigit()
    length = len(password) >= 8

    return upper and lower and number and length
