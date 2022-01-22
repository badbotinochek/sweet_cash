
import enum
from db import db
from api.models.base import BaseModel


class ParticipantEventRole(enum.Enum):
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
    role = db.Column(db.Enum(ParticipantEventRole), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.event_id = kwargs.get('event_id')
        self.role = kwargs.get('role')

    @classmethod
    def get_by_user(cls, event_id: int, user_id: int):
        participant = cls.query.filter(cls.id == event_id, cls.user_id == user_id, cls.accepted == True).first()
        return participant
