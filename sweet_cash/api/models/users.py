
import bcrypt

from sweet_cash.db import db
from sweet_cash.api.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    deleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.password = bcrypt.hashpw(kwargs.get('password').encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def update(self, **kwargs):
        if kwargs.get('name') is not None:
            self.name = kwargs.get('name')
        if kwargs.get('email') is not None:
            self.email = kwargs.get('email')
        if kwargs.get('phone') is not None:
            self.phone = kwargs.get('phone')
        if kwargs.get('confirmed') is not None:
            self.confirmed = kwargs.get('confirmed')
        db.session.commit()

    def __repr__(self):
        return "<User(name='{}', email='{}', password={}".format(self.name, self.email, self.password)

    @classmethod
    def get(cls, user_id: int) -> db.Model:
        user = cls.query.filter(cls.id == user_id).first()
        return user

    @classmethod
    def get_user(cls, email: str) -> db.Model:
        result = cls.query.filter(cls.email == email).first()
        return result

    def check_password(self, password: str) -> bool:
        result = bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        return result
