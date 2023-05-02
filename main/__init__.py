import os

import yaml
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

import settings
from main.custom_exceptions import CUSTOM_EXCEPTIONS
from main.custom_exceptions.exception_handlers import handle_exception
from main.db import db
from main.logging_module.logger import get_handler
from main.modules import api, jwt
from main.utils import construct_timedelta, log_user_access

yaml.add_constructor("!timedelta", construct_timedelta)  # handle timedelta in yaml file.


def get_app(env=None):
    app = Flask(__name__)
    if not env:
        env = os.environ.get("FLASK_ENV", "development")
    with open("config/config.yaml", "r") as f:
        config = yaml.load(Loader=yaml.Loader, stream=f)[env]
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
