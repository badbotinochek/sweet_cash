
from datetime import datetime

from db import db


class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        serialized_obj = {}
        for column in self.__table__.columns:
            serialized_obj[column.key] = self[column.key]
        return serialized_obj

    def create(self):
        db.session.add(self)
        db.session.commit()
