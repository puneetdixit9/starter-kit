from main.db import BaseModel, db


class Team(BaseModel):
    """
    Model for team.
    """

    __tablename__ = "team"
    name = db.Column(db.String(100), unique=True)
    tid = db.Column(db.String(100), unique=True)
