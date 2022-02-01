
from db import db
from api.models.base import BaseModel


class EventModel(BaseModel):
    __tablename__ = 'events'
    updated_at = db.Column(db.DateTime, nullable=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')

    @classmethod
    def get_by_user(cls, event_id: int, user_id: int):
        event = cls.query.filter(cls.id == event_id, cls.user_id == user_id).first()
        return event

    def get_id(self):
        return self.id