
from datetime import datetime
from flask_jwt_extended import create_access_token
from datetime import timedelta

from db import db


class SessionModel(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    login_method = db.Column(db.String, nullable=True)
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.token = self.new_token()
        self.user_id = kwargs.get('user_id')
        self.login_method = kwargs.get('login_method')

    def get_id(self):
        return self.id

    def get_token(self):
        return self.token

    def new_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, login_method: str):
        self.token = self.new_token()
        self.login_method = login_method
        self.updated_at = datetime.utcnow().isoformat()
        db.session.commit()

    @classmethod
    def get_user_id(cls, token: str):
        result = cls.query.filter(cls.token == token).first()
        if result is not None:
            return result.user_id
        return result

    @classmethod
    def get(cls, user_id=None, token=None):
        if user_id is not None:
            result = cls.query.filter(cls.user_id == user_id).first()
        elif token is not None:
            result = cls.query.filter(cls.token == token).first()
        else:
            result = None
        return result
