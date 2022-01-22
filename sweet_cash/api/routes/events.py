from flask import request, Blueprint
import logging

from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
from api.services.events.create_event import CreateEvent

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
