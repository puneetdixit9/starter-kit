from main.db import BaseModel, db


class Address(BaseModel):
    """
    Model for address.
    """

    __tablename__ = "address"

    type = db.Column(db.String(50), nullable=False)
    house_no_and_street = db.Column(db.String(50), nullable=False)
    landmark = db.Column(db.String(50))
    country = db.Column(db.String(50), nullable=False)
    pin_code = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.ForeignKey("auth_user.id"))

    user = db.relationship("AuthUser", backref=db.backref("addresses", lazy=True))

    def serialize(self) -> dict:
        """
        Override serialize function to add extra functionality
        :return:
        """
        dict_data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "user_id"}
        dict_data["username"] = self.user.username if self.user else None
        return dict_data
