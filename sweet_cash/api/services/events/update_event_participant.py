import logging

from sweet_cash.api.services.events.get_event_participant import GetEventParticipant
from sweet_cash.api.models.event_participants import EventParticipantsModel, EventParticipantRole
import sweet_cash.api.errors as error

logger = logging.getLogger(name="events")


class UpdateEventParticipant(object):
    get_event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> EventParticipantsModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        participant_id = kwargs.get("participant_id")
        role = kwargs.get("role")

        if not EventParticipantRole.has_value(role):
            logger.warning(f'User {user_id} is trying to create participant with invalid '
                           f'role {role}')
            raise error.APIParamError(f'Invalid participant role {role}')

        # Checking that user is the event manager
        self.get_event_participant(event_id=event_id,
                                   user_id=user_id,
                                   accepted=True,
                                   role='Manager')

        # Get event participant for user
        participant = self.get_event_participant(participant_id=participant_id)

        if participant.event_id != event_id:
            logger.warning(f'User {user_id} is trying to update participant {participant_id} form other event')
            raise error.APIParamError(f'Participant {participant_id} not in event {event_id}')

        if participant.user_id == user_id:
            logger.warning(f'User {user_id} is trying to update his participant {participant_id}')
            raise error.APIConflict(f'You cannot update your participant')

        participant.update(role=EventParticipantRole(role))

        logger.info(f'User {user_id} update event {event_id} with role {participant.role}')

        return participant
