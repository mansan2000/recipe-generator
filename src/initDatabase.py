from app import app
from database.database import db
from models.models import Recipe, User

with app.app_context():
    db.create_all()

    db.session.commit()
