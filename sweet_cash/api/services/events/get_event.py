import logging

from api.models.event import EventModel
import api.errors as error

logger = logging.getLogger(name="events")


class GetEvent:

    def __call__(self, event_id: int, user_id: int) -> EventModel:
        event = EventModel.get_by_user(event_id=event_id, user_id=int(user_id))

        if event is None:
            logger.warning(f'User {user_id} is trying to get a non-existent event {event_id}')
            raise error.APIValueNotFound(f'Event {event_id} not found for user {user_id}')

        logger.info(f'User {user_id} got event {event_id}')

        return event
