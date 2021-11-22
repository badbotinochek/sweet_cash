from datetime import datetime

from db import db
from api.models.base import BaseModel


class ReceiptModel(BaseModel):
    __tablename__ = 'receipts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    external_id = db.Column(db.String, index=True, nullable=False)
    transaction_id = db.Column(db.Integer, nullable=True)
    data = db.Column(db.JSON, nullable=True)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.external_id = kwargs.get('external_id')
        self.data = kwargs.get('data')

    @classmethod
    def get_by_user(cls, receipt_id: int, user_id: int):
        receipt = cls.query.filter(cls.external_id == receipt_id, cls.user_id == user_id).first()
        return receipt
