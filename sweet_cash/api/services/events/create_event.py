
import logging

from api.models.event import EventModel
from api.models.event_participants import EventParticipantsModel, EventParticipantRole
from api.services.events.create_event_participant import CreateEventParticipant
from api.services.events.confirm_event_participant import ConfirmEventParticipant
from api.api import str2datetime
import api.errors as error

logger = logging.getLogger(name="events")


class CreateEvent(object):
    create_participant = CreateEventParticipant()
    confirm_participant = ConfirmEventParticipant()

    def __call__(self, **kwargs) -> EventModel:
        user_id = kwargs.get("user_id")
        name = kwargs.get("name")
        start = kwargs.get("start")
        end = kwargs.get("end")
        description = kwargs.get("description")

        if start is not None and end is not None:
            if str2datetime(start) > str2datetime(end):
                raise error.APIParamError(f'Start {start} must be less than End {end}')

        event = EventModel(name=name,
                           start=start,
                           end=end,
                           description=description)

        event.create()

        event_id = event.get_id()

        # Create first participant for event
        participant = EventParticipantsModel(user_id=user_id,
                                             event_id=event_id,
                                             role=EventParticipantRole("Manager"))

        participant.create()

        # Confirm participant
        self.confirm_participant(user_id=user_id, event_id=event_id)

        logger.info(f'User {user_id} created event {event_id}')

        return event
