import logging

from api.models.event_users import EventUsersModel
import api.errors as error

logger = logging.getLogger(name="transactions")


class GetEventUser:

    def __call__(self, event_id: int, user_id: int) -> EventUsersModel:
        event_users = EventUsersModel.get_by_user(event_id=event_id, user_id=int(user_id))
        if event_users is None:
            logger.warning(f'User {user_id} is trying to get a non-existent event user {event_id}')
            raise error.APIValueNotFound(f'User {user_id} not found in event {event_id}')

        logger.info(f'User {user_id} got event user from event {event_id}')

        return event_users
