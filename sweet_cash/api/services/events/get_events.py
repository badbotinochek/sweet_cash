import logging

from api.models.event import EventModel

logger = logging.getLogger(name="events")


class GetEvents:

    def __call__(self, **kwargs) -> [EventModel]:
        pass
