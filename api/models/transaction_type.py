from db import db


class TransactionType(db.Model):
    __tablename__ = 'transactions_type'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    deleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, type_id: int):
        transaction_type = cls.query.filter(cls.id == type_id).first()
        return transaction_type

    @classmethod
    def get_name(cls, type_id: int):
        transaction_type = cls.query.filter(cls.id == type_id).first()
        if transaction_type is not None:
            return transaction_type.name
        return transaction_type
