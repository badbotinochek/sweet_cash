from flask import Blueprint
import logging

from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
from api.services.events.create_event import CreateEvent
from api.services.events.get_event import GetEvent
from api.services.events.update_event import UpdateEvent
from api.services.events.add_participant import AddParticipant
from api.services.events.update_participant import UpdateParticipant
from api.services.events.confirm_event import ConfirmEvent
from api.services.events.reject_event import RejectEvent

logger = logging.getLogger(name="events")

events_api = Blueprint('events', __name__)


@events_api.route('/api/v1/events', methods=['POST'])
@auth()
@jsonbody(name=features(type=str, required=True),
          start=features(type=str),
          end=features(type=str),
          description=features(type=str))
def create_event(name: str,
                 start=None,
                 end=None,
                 description=None,
                 create_event=CreateEvent()):
    result = formatting(create_event(name=name,
                                     start=start,
                                     end=end,
                                     description=description))

    return SuccessResponse(result)


@events_api.route('/api/v1/events', methods=['GET'])
@auth()
@query_params(limit=features(type=str),
              offset=features(type=str))
def get_events(limit=100, offset=0, get_events=GetEvent()):
    pass


@events_api.route('/api/v1/events/<int:event_id>', methods=['PUT'])
@auth()
@jsonbody(name=features(type=str, required=True),
          start=features(type=str),
          end=features(type=str),
          description=features(type=str))
def update_transaction(event_id: int,
                       name: str,
                       start=None,
                       end=None,
                       description=None,
                       update_event=UpdateEvent()):
    pass


@events_api.route('/api/v1/events/by_filter', methods=['GET'])
@auth()
def get_events(event_id: int, get_events=GetEvent()):
    pass


@events_api.route('/api/v1/events/<int:event_id>/participant', methods=['POST'])
@auth()
@jsonbody(user_id=features(type=int, required=True),
          role=features(type=str, required=True))
def add_participant(event_id: int,
                    name: str,
                    role: str,
                    add_participant=AddParticipant()):
    pass


@events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>', methods=['PUT'])
@auth()
@jsonbody(user_id=features(type=int, required=True),
          role=features(type=str, required=True))
def update_participant(event_id: int,
                       participant: int,
                       name: str,
                       role: str,
                       update_participant=UpdateParticipant()):
    pass


@events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>/confirm', methods=['PUT'])
@auth()
def confirm_event(event_id: int,
                  participant: int,
                  confirm_event=ConfirmEvent()):
    pass


@events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>/reject', methods=['PUT'])
@auth()
def reject_event(event_id: int,
                 participant: int,
                 reject_event=RejectEvent()):
    pass
