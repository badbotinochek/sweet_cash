import logging

from api.services.events.get_event_participant import GetEventParticipant
from api.models.event_participants import EventParticipantsModel

logger = logging.getLogger(name="events")


class ConfirmEventParticipant(object):
    get_event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> EventParticipantsModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")

        participant = self.get_event_participant(event_id=event_id, user_id=user_id, accepted=False)

        participant.accept()

        logger.info(f'User {user_id} confirm event {event_id} with role {participant.role}')

        return participant
