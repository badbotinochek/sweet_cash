import logging

from api.models.event_participants import EventParticipantsModel

logger = logging.getLogger(name="events")


class CreateEventParticipant:

    def __call__(self, **kwargs) -> EventParticipantsModel:
        pass

