from main.db import BaseModel, db


class LogEvent(BaseModel):
    """
    Model for log_event.
    """

    __tablename__ = "log_event"
    event_name = db.Column(db.String(100), nullable=True)
    path = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.String(100), nullable=True)
    tid = db.Column(db.String(100), nullable=True)
    is_success = db.Column(db.String(100), nullable=True)
    response_time = db.Column(db.String(100), nullable=True)
