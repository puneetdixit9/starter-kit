from project import get_app, db
import settings

app = get_app(settings.CONFIG)

with app.app_context():
    db.create_all()
    print("Tables created")
