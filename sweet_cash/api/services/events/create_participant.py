import logging

from api.models.event_users import EventUsersModel

logger = logging.getLogger(name="event_participant")


class CreateEventParticipant:

    def __call__(self, **kwargs) -> EventUsersModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        role = kwargs.get("role")
        accepted = kwargs.get("accepted")

        participant = EventUsersModel(user_id=user_id,
                                      event_id=event_id,
                                      role=role,
                                      accepted=accepted)

        participant.create()

        return participant

