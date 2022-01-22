import logging

from api.services.events.get_event_user import GetEventUser
from api.models.event import EventModel
from config import Config
import api.errors as error

logger = logging.getLogger(name="event")


class CreateEvent:
    event_user = GetEventUser()

    def __call__(self, **kwargs) -> EventModel:
        name = kwargs.get("name")
        start = kwargs.get("start")
        end = kwargs.get("end")
        description = kwargs.get("description")

        event = EventModel(name=name,
                           start=start,
                           end=end,
                           description=description)

        if description is not None:
            event.description = description

        event.create()

        logger.info(f'User created transaction {id}')

        return event
