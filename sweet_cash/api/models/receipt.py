from datetime import datetime

from db import db


class ReceiptModel(db.Model):
    __tablename__ = 'receipts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, index=True, nullable=False)
    external_id = db.Column(db.String, index=True, nullable=False)
    transaction_id = db.Column(db.Integer, nullable=True)
    data = db.Column(db.JSON, nullable=True)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.external_id = kwargs.get('external_id')
        self.data = kwargs.get('data')

    def get_id(self):
        return self.id

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_user(cls, receipt_id: int, user_id: int):
        receipt = cls.query.filter(cls.external_id == receipt_id, cls.user_id == user_id).first()
        return receipt
