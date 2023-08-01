from models.models import Recipe, User
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


def get_saved_recipes_from_database(user):
    allRows = Recipe.query.all()
    recipes_list = []
    dollarSign = "$"
    for recipe in allRows:
        if recipe.username == user:
            recipeName = f"{dollarSign}{recipe.recipe_name}{dollarSign}"
            full_recipe = recipeName + "\n" + recipe.instructions
            recipes_list.append(full_recipe)
    recipes_string = ""
    for i in recipes_list:
        recipes_string += i + "\n"
    return recipes_string
