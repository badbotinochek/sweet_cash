
import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

from db import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hashpw(kwargs.get('password').encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def __repr__(self):
        return "<User(name='{}', email='{}', password={}".format(self.name, self.email, self.password)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    def get_id(self):
        return self.id

    @classmethod
    def get_user(cls, email: str) -> db.Model:
        result = cls.query.filter(cls.email == email).first()
        return result

    def check_password(self, password: str) -> bool:
        result = bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
        return result
