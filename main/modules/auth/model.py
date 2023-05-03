from sqlalchemy import event

from main.db import BaseModel, db
from main.modules.user.model import User


class AuthUser(BaseModel):
    """
    Model for auth_user.
    """

    __tablename__ = "auth_user"

    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    mobile_number = db.Column(db.String(100), nullable=True)


@event.listens_for(AuthUser, "after_insert")
def auth_user_created_listener(mapper, connection, target):
    connection.execute(User.__table__.insert().values(id=target.id, username=target.username, email=target.email))
