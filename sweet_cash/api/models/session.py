
import uuid
from datetime import datetime
from flask_jwt_extended import create_access_token
from datetime import timedelta

from db import db
from api.models.base import BaseModel


class SessionModel(BaseModel):
    __tablename__ = 'sessions'
    updated_at = db.Column(db.DateTime, nullable=True)
    refresh_token = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    login_method = db.Column(db.String, nullable=True)
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, **kwargs):
        self.refresh_token = self._new_refresh_token()
        self.token = self._new_token()
        self.user_id = kwargs.get('user_id')
        self.login_method = kwargs.get('login_method')

    @staticmethod
    def _new_refresh_token():
        refresh_token = uuid.uuid4()
        return refresh_token

    def _new_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    def update(self, login_method=None):
        self.refresh_token = self._new_refresh_token()
        self.token = self._new_token()
        self.updated_at = datetime.utcnow().isoformat()
        if login_method is not None:
            self.login_method = login_method
        db.session.commit()

    @classmethod
    def get_user_id(cls, token: str):
        result = cls.query.filter(cls.token == token).first()
        if result is not None:
            return result.user_id
        return result

    @classmethod
    def get(cls, user_id=None, refresh_token=None):
        if user_id is not None:
            result = cls.query.filter(cls.user_id == user_id).first()
        elif refresh_token is not None:
            result = cls.query.filter(cls.refresh_token == refresh_token).first()
        else:
            result = None
        return result
