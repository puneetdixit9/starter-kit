import settings
import logging
import os

from flask import Flask
from flask_cors import CORS
from src.database import db
from src.managers import jwt
from src.routers import APP_BLUEPRINTS
from src.custom_exceptions import CUSTOM_EXCEPTIONS
from src.custom_exceptions.exception_handlers import handle_exception

if not os.path.exists('logs'):
    os.makedirs('logs')

handler = logging.FileHandler('logs/flask.log')
handler.setLevel(logging.ERROR)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))


def get_app(config):
    app = Flask(__name__)

    app.config.update(config)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # register all blueprints
    for blueprint in APP_BLUEPRINTS:
        app.register_blueprint(blueprint)

    # register all custom custom_exceptions
    for exc in CUSTOM_EXCEPTIONS:
        app.register_error_handler(exc[0], exc[1])

    app.logger.addHandler(handler)
    app.register_error_handler(Exception, lambda e: handle_exception(e, app))

    return app


if __name__ == "__main__":
    get_app(settings.CONFIG).run(debug=True)
