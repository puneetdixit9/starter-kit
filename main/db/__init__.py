from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=None, onupdate=db.func.now())

    @classmethod
    def create(cls, data: dict) -> db.Model:
        """
        To create the record.
        :param data:
        :return:
        """
        record = cls(**data)
        db.session.add(record)
        db.session.commit()
        return record

    def update(self, data: dict):
        """
        To update the record.
        :param data:
        :return:
        """
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        db.session.commit()

    @classmethod
    def delete(cls, **filters):
        """
        To delete the records based on filters.
        :param filters:
        :return:
        """
        db.session.query(cls).filter_by(**filters).delete()
        db.session.commit()

    def serialize(self) -> dict:
        """
        To convert the model object to a dict.
        :return:
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
