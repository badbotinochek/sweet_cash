import logging

from api.services.events.get_event_participant import GetEventParticipant
from api.models.event import EventModel
import api.errors as error

logger = logging.getLogger(name="events")


class GetEvents:
    event_participant = GetEventParticipant()

    @staticmethod
    def _ids2list(ids):
        if type(ids) is list:
            return ids

        ids_list = []

        if ids is None:
            return ids_list

        split_list = ids.split(',')

        for elem in split_list:
            try:
                ids_list.append(int(elem))
            except ValueError:
                continue

        return ids_list

    def __call__(self, **kwargs) -> [EventModel]:
        user_id = kwargs.get("user_id")
        event_ids = self._ids2list(kwargs.get("event_ids"))

        events = []
        for event_id in event_ids:
            # Checking that user is a participant in event
            self.event_participant(event_id=event_id, user_id=user_id)

            # Get event
            event = EventModel.get_by_id(event_id=event_id)

            if event is None:
                logger.warning(f'User {user_id} is trying to get a non-existent event {event_id}')
                raise error.APIValueNotFound(f'Event {event_id} not found for user {user_id}')

            events.append(event)

        logger.info(f'User {user_id} got events {event_ids}')

        return events
