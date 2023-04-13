import settings
from server import get_app
from src.database import db

app = get_app(settings.CONFIG)


with app.app_context():
    db.create_all()
    print("Tables created")
