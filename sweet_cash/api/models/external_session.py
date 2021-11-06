
from datetime import datetime

from db import db


class NalogRuSessionModel(db.Model):
    __tablename__ = 'nalog_ru_sessions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    session_id = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=True)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.refresh_token = kwargs.get('refresh_token')

    def get_id(self):
        return self.id

    def get_session_id(self):
        return self.session_id

    def get_refresh_token(self):
        return self.refresh_token

    @classmethod
    def get_by_user(cls, user_id: int):
        session = cls.query.filter(cls.user_id == user_id).first()
        return session
