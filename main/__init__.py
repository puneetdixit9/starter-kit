from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

import settings
from main.custom_exceptions import CUSTOM_EXCEPTIONS
from main.custom_exceptions.exception_handlers import handle_exception
from main.db import db
from main.logging_module.logger import get_handler
from main.modules import api, jwt
from src.utils import log_user_access


def get_app(config):
    app = Flask(__name__)

    app.config.update(config)
    CORS(app)
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # register all custom custom_exceptions
    for exc in CUSTOM_EXCEPTIONS:
        app.register_error_handler(exc[0], exc[1])

    app.logger.addHandler(get_handler("exceptions", settings.ERROR))
    app.after_request(log_user_access)
    app.register_error_handler(Exception, lambda e: handle_exception(e, app))

    return app
