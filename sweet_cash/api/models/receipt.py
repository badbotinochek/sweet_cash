from datetime import datetime

from db import db
from api.models.base import BaseModel


class ReceiptModel(BaseModel):
    __tablename__ = 'receipts'
    user_id = db.Column(db.Integer, index=True, nullable=False)
    external_id = db.Column(db.String, index=True, nullable=False)
    data = db.Column(db.JSON, nullable=True)
    deleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.external_id = kwargs.get('external_id')
        self.data = kwargs.get('data')

    @classmethod
    def get_by_external_id(cls, external_id: str, user_id: int):
        receipt = cls.query.filter(cls.external_id == external_id, cls.user_id == user_id).first()
        return receipt
