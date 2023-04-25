import settings
from main import get_app
from main.db import db

app = get_app(settings.CONFIG)


with app.app_context():
    db.create_all()
    print("Tables created")
