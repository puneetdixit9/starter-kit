import settings

from flask import Flask
from flask_cors import CORS
from src.database import db
from src.managers import jwt
from src.routers import APP_BLUEPRINTS


def get_app(config):
    app = Flask(__name__)

    app.config.update(config)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # register all blueprints
    for blueprint in APP_BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app


if __name__ == "__main__":
    get_app(settings.CONFIG).run(debug=True)
