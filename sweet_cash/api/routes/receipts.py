from flask import request, Blueprint
import logging

from api.services.receipts import Receipt
from api.api import Response, auth, jsonbody, query_params, features

logger = logging.getLogger(name="receipts")

receipts_api = Blueprint('receipts', __name__)


@receipts_api.route('/api/v1/receipts/qr', methods=['POST'])
@auth()
@jsonbody(qr=features(type=str, required=True))
def save_receipt(qr: str):
    result = Receipt(user_id=getattr(request, "user_id"),
                     qr=qr).create()
    return Response.success(result)
