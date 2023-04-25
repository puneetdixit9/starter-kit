import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.expanduser("~"), "Desktop", "starter_app.env")
load_dotenv(dotenv_path)


SECRET_KEY = "test"
TOKEN_EXPIRE_IN = 360

CONFIG = {
    "SECRET_KEY": os.environ.get("SECRET_KEY"),
    "SQLALCHEMY_DATABASE_URI": os.environ.get("SQLALCHEMY_DATABASE_URI"),
    "JWT_SECRET_KEY": os.environ.get("JWT_SECRET_KEY"),
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_TIME"))),
    "JWT_REFRESH_TOKEN_EXPIRES": timedelta(minutes=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_TIME"))),
    "SQLALCHEMY_POOL_SIZE": 10,
    "SQLALCHEMY_MAX_OVERFLOW": 5,
    "SQLALCHEMY_ECHO": True,
}

TEST_CONFIG = CONFIG.copy()
TEST_CONFIG["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")


LOGS_BASE_DIR = "logs"
if not os.path.exists(LOGS_BASE_DIR):
    os.makedirs(LOGS_BASE_DIR)
ERROR = logging.ERROR
INFO = logging.INFO
WARNING = logging.WARNING
