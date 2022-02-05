import logging

from api.models.event_participants import EventParticipantsModel, EventParticipantRole
import api.errors as error

logger = logging.getLogger(name="events")


class GetEventParticipant:

    def __call__(self, **kwargs) -> EventParticipantsModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        accepted = kwargs.get("accepted")
        role = kwargs.get("role")
        participant_id = kwargs.get("participant_id")

        if participant_id is not None:
            event_participant = EventParticipantsModel.get_by_id(participant_id=participant_id)
        else:
            event_participant = EventParticipantsModel.get_by_event_and_user(event_id=event_id, user_id=user_id)

        if event_participant is None:
            logger.warning(f'Trying to get a non-existent event participant {user_id}')
            raise error.APIValueNotFound(f'Participant {participant_id} not found')

        if accepted is not None and event_participant.accepted is not accepted:
            if accepted:
                logger.warning(f'Trying to get a non-existent accepted event participant {user_id} '
                               f'from event {event_id}')
                raise error.APIValueNotFound(f'Accepted user {user_id} not found in event {event_id}')
            else:
                logger.warning(f'Trying to get a non-existent non accepted event participant {user_id} '
                               f'from event {event_id}')
                raise error.APIValueNotFound(f'Non accepted user {user_id} not found in event {event_id}')

        if role is not None and event_participant.role != EventParticipantRole(role):
            logger.warning(f'Trying to get a non-existent event participant {user_id} with {role} '
                           f'from event {event_id}')
            raise error.APIValueNotFound(f'User {user_id} with {role} not found in event {event_id}')

        logger.info(f'User {user_id} got event user from event {event_id}')

        return event_participant
