from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from src.database.models.auth import User, TokenBlocklist
from src.database.models.main import Address
