from models.models import Recipe
from database.database import db


def insert_row(user, recipe, instructions):
    newRow = Recipe(user, recipe, instructions)
    db.session.add(newRow)
    db.session.commit()
