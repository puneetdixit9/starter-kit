from flask import Flask
from flask_cors import CORS

import settings
from src.custom_exceptions import CUSTOM_EXCEPTIONS
from src.custom_exceptions.exception_handlers import handle_exception
from src.database import db
from src.logging_module.logger import get_handler
from src.managers.jwt import jwt
from src.routers import APP_BLUEPRINTS
from src.utils import log_user_access


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

    if not config.get("TESTING"):
        app.logger.addHandler(get_handler("exceptions", settings.ERROR))
        app.after_request(log_user_access)
    app.register_error_handler(Exception, lambda e: handle_exception(e, app))

    return app


if __name__ == "__main__":
    get_app(settings.CONFIG).run(debug=True)
