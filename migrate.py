from src.database import db
import settings
from server import get_app

app = get_app(settings.CONFIG)

with app.app_context():
    db.create_all()
    print("Tables created")
