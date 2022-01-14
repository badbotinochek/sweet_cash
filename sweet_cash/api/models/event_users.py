
import enum
from db import db
from api.models.base import BaseModel


class UserEventRole(enum.Enum):
    MANAGER = "Manager"
    OBSERVER = "Observer"
    PARTNER = "Partner"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class EventUsersModel(BaseModel):
    __tablename__ = 'events_users'
    updated_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    event_id = db.Column(db.Integer, index=True, nullable=False)
    role = db.Column(db.Enum(UserEventRole), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.event_id = kwargs.get('event_id')
        self.role = kwargs.get('role')

    @classmethod
    def get_by_user(cls, event_id: int, user_id: int):
        event_user = cls.query.filter(cls.id == event_id, cls.user_id == user_id, cls.accepted == True).first()
        return event_user
