import logging

from api.models.event_participants import EventParticipantsModel

logger = logging.getLogger(name="events")


class UpdateEventParticipant:

    def __call__(self, **kwargs) -> EventParticipantsModel:
        pass
