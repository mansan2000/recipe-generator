from app import app
from database.database import db
from models.models import Recipe, User

with app.app_context():
    db.create_all()
    recipe1 = Recipe("test","test","test")
    user1 = User("test", "test", "test", "test", "test")

    db.session.add_all([recipe1])

    db.session.commit()
