from flask import request
import logging

from api.models.event import EventModel
from api.services.events.create_participant import CreateEventParticipant

logger = logging.getLogger(name="event")


class CreateEvent:
    create_participant = CreateEventParticipant()

    def __call__(self, **kwargs) -> EventModel:
        name = kwargs.get("name")
        start = kwargs.get("start")
        end = kwargs.get("end")
        description = kwargs.get("description")

        event = EventModel(name=name,
                           start=start,
                           end=end,
                           description=description)

        event.create()

        user_id = getattr(request, "user_id")

        self.create_participant(user_id=user_id,
                                event_id=event.get_id(),
                                role="MANAGER")
        # Подтвердить менеджера

        logger.info(f'User {user_id} created event {id}')

        return event
