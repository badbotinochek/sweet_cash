import logging

from api.models.event import EventModel
from api.models.event_participants import EventParticipantsModel, EventParticipantRole
import api.errors as error

logger = logging.getLogger(name="events")


class GetEventsByFilter(object):

    @staticmethod
    def _roles2list(roles: str):

        if roles is None:
            return None

        roles_list = []

        roles_split = roles.split(',')

        for role in roles_split:

            if not EventParticipantRole.has_value(role):
                raise error.APIParamError(f'Invalid participant role {role}')

            roles_list.append(EventParticipantRole(role))

        return roles_list

    def __call__(self, **kwargs) -> [EventModel]:
        user_id = kwargs.get("user_id")
        roles = self._roles2list(kwargs.get("role"))
        accepted = kwargs.get("accepted")

        # Get event participants
        if roles is not None:
            # Get accepted participants for roles
            participants = EventParticipantsModel.get_by_user_role(user_id=user_id, roles=roles)
        else:
            participants = EventParticipantsModel.get_by_user(user_id=user_id, accepted=accepted)

        # Get event_ids from participants
        event_ids = []
        for participant in participants:
            event_ids.append(participant.event_id)

        # Get all existing events
        events = EventModel.get_by_ids(event_ids=event_ids)

        logger.info(f'User {user_id} got events')

        return events
