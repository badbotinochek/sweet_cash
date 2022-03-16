
from datetime import datetime

from sweet_cash.db import db
from sweet_cash.api.models.base import BaseModel
from sweet_cash.api.models.event_participants import EventParticipantsModel


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

    def update(self, **kwargs):
        self.updated_at = datetime.utcnow().isoformat()
        self.name = kwargs.get('name')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.description = kwargs.get('description')
        db.session.commit()

    @classmethod
    def get_by_id(cls, event_id: int):
        event = cls.query.filter(cls.id == event_id).first()
        return event

    @classmethod
    def get_by_ids(cls, event_ids: [int]):
        events = cls.query.filter(cls.id.in_(event_ids)).all()
        return events

    def get_id(self):
        return self.id

    def get_participants(self):
        participants = EventParticipantsModel.get_by_event(event_id=self.id)
        return participants
