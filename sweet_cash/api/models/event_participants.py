
import enum
from datetime import datetime

from sweet_cash.db import db
from sweet_cash.api.models.base import BaseModel


class EventParticipantRole(enum.Enum):
    MANAGER = "Manager"
    OBSERVER = "Observer"
    PARTNER = "Partner"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class EventParticipantsModel(BaseModel):
    __tablename__ = 'events_participants'
    updated_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    event_id = db.Column(db.Integer, index=True, nullable=False)
    role = db.Column(db.Enum(EventParticipantRole), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.event_id = kwargs.get('event_id')
        self.role = kwargs.get('role')

    def update(self, **kwargs):
        self.updated_at = datetime.utcnow().isoformat()
        self.role = kwargs.get('role')
        db.session.commit()

    @classmethod
    def get_by_id(cls, participant_id: int):
        participant = cls.query.filter(cls.id == participant_id).first()
        return participant

    @classmethod
    def get_by_event_and_user(cls, event_id: int, user_id: int):
        participant = cls.query.filter(cls.event_id == event_id, cls.user_id == user_id).first()
        return participant

    @classmethod
    def get_by_event(cls, event_id: int):
        participants = cls.query.filter(cls.event_id == event_id).all()
        return participants

    @classmethod
    def get_by_user(cls, user_id: int, accepted: bool):
        participants = cls.query.filter(cls.user_id == user_id, cls.accepted == accepted).all()
        return participants

    @classmethod
    def get_by_user_role(cls, user_id: int, roles: [EventParticipantRole]):
        participants = cls.query.filter(cls.user_id == user_id, cls.role.in_(roles), cls.accepted == True).all()
        return participants

    def accept(self):
        self.accepted = True
        db.session.commit()

    @classmethod
    def delete(cls, participant_id: int):
        result = cls.query.filter(cls.id == participant_id).delete()
        return result
