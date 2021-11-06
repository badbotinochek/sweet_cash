
import bcrypt
from datetime import datetime

from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.password = bcrypt.hashpw(kwargs.get('password').encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def __repr__(self):
        return "<User(name='{}', email='{}', password={}".format(self.name, self.email, self.password)

    def get_id(self):
        return self.id

    def get_phone(self):
        return self.phone

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, user_id: str) -> db.Model:
        user = cls.query.filter(cls.id == user_id).first()
        return user

    @classmethod
    def get_user(cls, email: str) -> db.Model:
        result = cls.query.filter(cls.email == email).first()
        return result

    def check_password(self, password: str) -> bool:
        result = bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        return result
