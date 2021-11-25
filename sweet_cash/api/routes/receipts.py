from flask import request, Blueprint
import logging

from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
from api.dependencies import create_receipt_by_qr_

logger = logging.getLogger(name="receipts")

receipts_api = Blueprint('receipts', __name__)


@receipts_api.route('/api/v1/receipts/qr', methods=['POST'])
@auth()
@jsonbody(qr=features(type=str, required=True))
def save_receipt(qr: str):
    result = formatting(create_receipt_by_qr_(user_id=getattr(request, "user_id"),
                                              qr=qr)())
    return SuccessResponse(result)
