import settings

from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

jwt = JWTManager()


def get_app(config):
    app = Flask(__name__)

    app.config.update(config)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=settings.TOKEN_EXPIRE_IN)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # blueprint for auth routes
    from project.routers.auth import auth_router
    app.register_blueprint(auth_router)

    # blueprint for main routes
    from project.routers.main import main_router
    app.register_blueprint(main_router)

    return app
