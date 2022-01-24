import logging

from api.models.event import EventModel

logger = logging.getLogger(name="event_participant")


class RejectEvent:

    def __call__(self, **kwargs) -> EventModel:
        pass