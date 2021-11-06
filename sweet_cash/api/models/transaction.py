
from datetime import datetime

from db import db


class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    private = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(250), nullable=True)

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.user_id = kwargs.get('user_id')
        self.category = kwargs.get('category')
        self.amount = kwargs.get('amount')
        self.transaction_date = kwargs.get('transaction_date')
        self.private = kwargs.get('private')
        self.description = kwargs.get('description')

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        self.type = kwargs.get('type_id')
        self.category = kwargs.get('category_id')
        self.amount = kwargs.get('amount')
        self.transaction_date = kwargs.get('transaction_date')
        self.private = kwargs.get('private')
        if kwargs.get('description') is not None:
            self.description = kwargs.get('description')
        db.session.commit()

    @classmethod
    def get(cls, transaction_id: int, user_id: int):
        transaction = cls.query.filter(cls.id == transaction_id, cls.user_id == user_id).first()
        return transaction

    @classmethod
    def get_transactions(cls, user_id: int, offset=0, limit=100):
        query = cls.query.filter(cls.user_id == user_id)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(limit * offset)
        return query

    @classmethod
    def delete_transaction(cls, transaction_id: int):
        cls.query.filter(cls.id == transaction_id).delete()
        db.session.commit()
