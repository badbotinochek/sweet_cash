
from db import db
from api.models.base import BaseModel


class TransactionCategory(BaseModel):
    __tablename__ = 'transactions_categories'
    name = db.Column(db.String, nullable=False)
    parent_category_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(250), nullable=True)
    deleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.parent_category_id = kwargs.get('parent_category_id')
        self.description = kwargs.get('description')

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, category_id: int):
        transaction_category = cls.query.filter(cls.id == category_id).first()
        return transaction_category

    @classmethod
    def get_name(cls, category_id: int):
        transaction_category = cls.query.filter(cls.id == category_id).first()
        if transaction_category is not None:
            return transaction_category.name
        return transaction_category

    @classmethod
    def get_transaction_categories(cls, offset=0, limit=100):
        query = cls.query.filter(cls.deleted == None)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(limit * offset)
        return query
