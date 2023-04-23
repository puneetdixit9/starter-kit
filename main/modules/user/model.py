from main.db import BaseModel, db


class User(BaseModel):
    """
    Model for user.
    """

    __tablename__ = "user"

    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    function = db.Column(db.String(100), nullable=True)
