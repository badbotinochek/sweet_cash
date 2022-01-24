import logging

from api.models.event_participants import EventParticipantsModel

logger = logging.getLogger(name="event_participant")


class CreateEventParticipant:

    def __call__(self, **kwargs) -> EventParticipantsModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        role = kwargs.get("role")

        participant = EventParticipantsModel(user_id=user_id,
                                             event_id=event_id,
                                             role=role)

        participant.create()

        return participant
