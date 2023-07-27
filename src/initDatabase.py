from app import app
from database.database import db
from models.models import Recipe

with app.app_context():
    db.create_all()
    recipe1 = Recipe("mansan", "cook it yourself", "cook this for me?", "blank", "blank", "blank")

    db.session.add_all([recipe1])

    db.session.commit()
