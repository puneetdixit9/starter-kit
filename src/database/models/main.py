from datetime import datetime
from src.database import db


class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    house_no_and_street = db.Column(db.String, nullable=False)
    landmark = db.Column(db.String)
    country = db.Column(db.String, nullable=False)
    pin_code = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('addresses', lazy=True))

    def as_dict(self):
        dict_data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name is not "user_id"}
        dict_data["username"] = self.user.username if self.user else None
        return dict_data
    