import settings
from main import get_app

app = get_app(settings.CONFIG)


if __name__ == "__main__":
    app.run(debug=True)

#
# from main.db import db
# from main import get_app
# import settings
#
# app = get_app(settings.CONFIG)
#
# with app.app_context():
#     db.create_all()
#     print("Tables created")
