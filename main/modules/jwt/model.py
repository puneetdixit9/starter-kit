from main.db import BaseModel, db


class TokenBlocklist(BaseModel):
    """
    This model is used to store revoked tokens.
    """

    __tablename__ = "token_block_list"

    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
