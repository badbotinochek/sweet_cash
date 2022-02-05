import logging

from api.services.events.get_event_participant import GetEventParticipant
from api.services.users.get_user import GetUser
from api.models.event_participants import EventParticipantsModel, EventParticipantRole
import api.errors as error

logger = logging.getLogger(name="events")


class CreateEventParticipant:
    get_user = GetUser()
    event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> EventParticipantsModel:
        request_user_id = kwargs.get("request_user_id")
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        role = kwargs.get("role")

        if not EventParticipantRole.has_value(role):
            logger.warning(f'User {user_id} is trying to create participant with invalid '
                           f'role {role}')
            raise error.APIParamError(f'Invalid participant role {role}')

        # Checking user exist
        self.get_user(user_id=user_id)

        # Checking that user from request is the event manager
        self.event_participant(event_id=event_id,
                               user_id=request_user_id,
                               accepted=True,
                               role='Manager')

        # Checking that user is not event participant
        participant = EventParticipantsModel.get_by_event_and_user(event_id=event_id, user_id=int(user_id))

        if participant is not None:
            logger.warning(f'User {request_user_id} is trying to create existing event participant {user_id} '
                           f'from event {event_id}')
            raise error.APIParamError(f'Participant for {user_id} already exist in event {event_id}')

        participant = EventParticipantsModel(user_id=user_id,
                                             event_id=event_id,
                                             role=EventParticipantRole(role))

        participant.create()

        logger.info(f'User {user_id} added to event {event_id} with role {role}')

        return participant
