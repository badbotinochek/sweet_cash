from db import db


class TransactionCategory(db.Model):
    __tablename__ = 'transactions_category'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
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
    def get_transactions_categories(cls):
        query = cls.query.filter()
        return query
