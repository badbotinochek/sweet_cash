import logging

from sweet_cash.api.services.events.get_event_participant import GetEventParticipant
from sweet_cash.api.models.event import EventModel
from sweet_cash.api.api import ids2list
import sweet_cash.api.errors as error

logger = logging.getLogger(name="events")


class GetEvents(object):
    get_event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> [EventModel]:
        user_id = kwargs.get("user_id")
        event_ids = ids2list(kwargs.get("event_ids"))

        events = []
        for event_id in event_ids:
            # Checking that user is a participant in event
            self.get_event_participant(event_id=event_id, user_id=user_id)

            # Get event
            event = EventModel.get_by_id(event_id=event_id)

            if event is None:
                logger.warning(f'User {user_id} is trying to get a non-existent event {event_id}')
                raise error.APIValueNotFound(f'Event {event_id} not found for user {user_id}')

            events.append(event)

        logger.info(f'User {user_id} got events {event_ids}')

        return events
