import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import config_by_name
from main.cache import cache
from main.db import db
from main.exceptions import CUSTOM_EXCEPTIONS
from main.exceptions.handlers import handle_exception
from main.logger import ERROR, get_handler
from main.modules import api, jwt
from main.utils import log_user_access


def get_app(env=None, config=None):
    app = Flask(__name__)

    if not config:
        if not env:
            env = os.environ.get("FLASK_ENV", "dev")
        config = config_by_name[env]

    app.config.update(config)
    CORS(app)
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app, config=config_by_name["cache"])
    Migrate(app, db)

    # register all custom exceptions
    for exc in CUSTOM_EXCEPTIONS:
        app.register_error_handler(exc[0], exc[1])

    app.logger.addHandler(get_handler("exceptions", ERROR))
    app.after_request(log_user_access)
    app.register_error_handler(Exception, lambda e: handle_exception(e, app))

    return app
