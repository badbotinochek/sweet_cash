from flask import request, Blueprint
import logging

from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
from api.services.events.create_event import CreateEvent
from api.services.events.get_events import GetEvents
from api.services.events.update_event import UpdateEvent
from api.services.events.update_event_participant import UpdateEventParticipant
from api.services.events.confirm_event import ConfirmEvent
from api.services.events.reject_event import RejectEvent
from api.services.events.create_event_participant import CreateEventParticipant

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
    result = formatting(create_event(user_id=getattr(request, "user_id"),
                                     name=name,
                                     start=start,
                                     end=end,
                                     description=description))
    return SuccessResponse(result)


@events_api.route('/api/v1/events', methods=['GET'])
@auth()
@query_params(ids=features(type=str),
              role=features(type=str),
              accepted=features(type=str))
def get_events(ids: str,
               role: str,
               accepted: str,
               get_events=GetEvents()):
    events = get_events(user_id=getattr(request, "user_id"),
                        ids=ids,
                        role=role,
                        accepted=accepted)
    result = [formatting(item) for item in events]
    return SuccessResponse(result)


@events_api.route('/api/v1/events/<int:event_id>', methods=['PUT'])
@auth()
@jsonbody(name=features(type=str),
          start=features(type=str),
          end=features(type=str),
          description=features(type=str))
def update_event(event_id: int,
                 name: str,
                 start=None,
                 end=None,
                 description=None,
                 update_event=UpdateEvent()):
    result = formatting(update_event(user_id=getattr(request, "user_id"),
                                     event_id=event_id,
                                     name=name,
                                     start=start,
                                     end=end,
                                     description=description))
    return SuccessResponse(result)


@events_api.route('/api/v1/events/<int:event_id>/participant', methods=['POST'])
@auth()
@jsonbody(participant_id=features(type=int, required=True),
          role=features(type=str, required=True))
def add_participant(event_id: int,
                    participant_id: int,
                    role: str,
                    add_participant=CreateEventParticipant()):
    result = formatting(add_participant(user_id=getattr(request, "user_id"),
                                        event_id=event_id,
                                        participant_id=participant_id,
                                        role=role))
    return SuccessResponse(result)


@events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>', methods=['PUT'])
@auth()
@jsonbody(role=features(type=int, required=True))
def update_participant(event_id: int,
                       participant_id: int,
                       role: str,
                       update_participant=UpdateEventParticipant()):
    result = formatting(update_participant(user_id=getattr(request, "user_id"),
                                           event_id=event_id,
                                           participant_id=participant_id,
                                           role=role))
    return SuccessResponse(result)


@events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>/confirm', methods=['PUT'])
@auth()
def confirm_event(event_id: int,
                  participant_id: int,
                  confirm_event=ConfirmEvent()):
    result = formatting(confirm_event(user_id=getattr(request, "user_id"),
                                      event_id=event_id,
                                      participant_id=participant_id))
    return SuccessResponse(result)


@events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>/reject', methods=['PUT'])
@auth()
def reject_event(event_id: int,
                 participant_id: int,
                 reject_event=RejectEvent()):
    result = formatting(reject_event(user_id=getattr(request, "user_id"),
                                     event_id=event_id,
                                     participant_id=participant_id))
    return SuccessResponse(result)
