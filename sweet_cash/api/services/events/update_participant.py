import logging

from api.models.event_participants import EventParticipantsModel

logger = logging.getLogger(name="event_participant")


class UpdateParticipant:

    def __call__(self, **kwargs) -> EventParticipantsModel:
        pass