from flask import request
import logging

from api.models.event import EventModel
from api.services.events.create_participant import CreateEventParticipant

logger = logging.getLogger(name="event")

class CreateEvent:

    def __call__(self, **kwargs) -> EventModel:
        name = kwargs.get("name")
        start = kwargs.get("start")
        end = kwargs.get("end")
        description = kwargs.get("description")

        event = EventModel(name=name,
                           start=start,
                           end=end,
                           description=description)
        user_id = getattr(request, "user_id")

        event.create()
        global t
        t = event.get_id()
        self._create_manager()

        logger.info(f'User {user_id} created event {id}')

        return event

    def _create_manager(self,  create_participant=CreateEventParticipant()):
        user_id = getattr(request, "user_id")
        event_id = t
        role = "MANAGER"
        accepted = True

        manager = create_participant(user_id=user_id,
                                     event_id=event_id,
                                     role=role,
                                     accepted=accepted)

        return manager
