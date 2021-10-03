from db import db


class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer(150), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    count = db.Column(db.Integer(150), nullable=False)

    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.name = kwargs.get('name')
        self.count = kwargs.get('count')

