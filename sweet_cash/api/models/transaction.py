
import enum
from datetime import datetime

from db import db
from api.models.base import BaseModel


class TransactionType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class TransactionModel(BaseModel):
    __tablename__ = 'transactions'
    updated_at = db.Column(db.DateTime, nullable=True)
    number = db.Column(db.Integer, db.Sequence('transaction_num', start=1, increment=1))
    user_id = db.Column(db.Integer, index=True, nullable=False)
    event_id = db.Column(db.Integer, index=True, nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    receipt_id = db.Column(db.Integer, nullable=True)
    deleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.event_id = kwargs.get('event_id')
        self.type = kwargs.get('type')
        self.category = kwargs.get('category')
        self.amount = kwargs.get('amount')
        self.transaction_date = kwargs.get('transaction_date')
        self.description = kwargs.get('description')
        self.receipt_id = kwargs.get('receipt_id')

    def update(self, **kwargs):
        self.updated_at = datetime.utcnow().isoformat()
        self.type = kwargs.get('type')
        self.category = kwargs.get('category')
        self.amount = kwargs.get('amount')
        self.transaction_date = kwargs.get('transaction_date')
        self.receipt_id = kwargs.get('receipt_id')
        if kwargs.get('description') is not None:
            self.description = kwargs.get('description')
        db.session.commit()

    @classmethod
    def get_by_id(cls, transaction_id: int):
        transaction = cls.query.filter(cls.id == transaction_id).first()
        return transaction

    @classmethod
    def get_by_user(cls, transaction_id: int, user_id: int):
        transaction = cls.query.filter(cls.id == transaction_id, cls.user_id == user_id).first()
        return transaction

    @classmethod
    def get_transactions_by_user_id(cls, user_id: int, start: str, end: str, offset=0, limit=100):
        query = cls.query.filter(cls.user_id == user_id, cls.transaction_date >= start, cls.transaction_date <= end)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(limit * offset)
        return query

    @classmethod
    def get_transactions_by_event_id(cls, event_id: int, start: str, end: str, offset=0, limit=100):
        query = cls.query.filter(cls.event_id == event_id, cls.transaction_date >= start, cls.transaction_date <= end)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(limit * offset)
        return query

    @classmethod
    def delete_transaction(cls, transaction_id: int) -> int:
        num_rows_deleted = cls.query.filter(cls.id == transaction_id).delete()
        db.session.commit()
        return num_rows_deleted
