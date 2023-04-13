from datetime import datetime

from src.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    function = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(100), nullable=True)
    mobile_number = db.Column(db.String(100), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey("user.id"),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        nullable=False,
    )
