import logging

from api.services.events.get_events import GetEvents
from api.services.events.get_event_participant import GetEventParticipant
from api.models.event import EventModel
from api.models.event_participants import EventParticipantRole
from api.api import str2datetime
import api.errors as error

logger = logging.getLogger(name="events")


class UpdateEvent:
    get_events = GetEvents()
    event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> EventModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        name = kwargs.get("name")
        start = kwargs.get("start")
        end = kwargs.get("end")
        description = kwargs.get("description")

        if start is not None or end is not None:
            if str2datetime(start) > str2datetime(end):
                raise error.APIParamError(f'Start {start} must be less than End {end}')

        # Get event
        event = self.get_events(user_id=user_id, event_ids=[event_id])[0]

        # Checking that user is the event manager
        self.event_participant(event_id=event_id,
                               user_id=user_id,
                               accepted=True,
                               role='Manager')

        event.update(name=name,
                     start=start,
                     end=end,
                     description=description)

        logger.info(f'User {user_id} updated event {event.id}')

        return event
