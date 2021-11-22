
from datetime import datetime

from db import db
from api.models.base import BaseModel


class NalogRuSessionModel(BaseModel):
    __tablename__ = 'nalog_ru_sessions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    session_id = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=True, default=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.refresh_token = kwargs.get('refresh_token')

    def update(self, **kwargs):
        self.session_id = kwargs.get('session_id')
        self.refresh_token = kwargs.get('refresh_token')
        self.updated_at = datetime.utcnow().isoformat()
        db.session.commit()

    @classmethod
    def get_by_user(cls, user_id: int):
        session = cls.query.filter(cls.user_id == user_id).first()
        return session
