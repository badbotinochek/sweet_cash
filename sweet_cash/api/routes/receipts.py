from flask import request, Blueprint
import logging

from sweet_cash.api.api import SuccessResponse, auth, jsonbody, features, formatting
from sweet_cash.api.services.receipts.create_receipt_by_qr import CreateReceiptByQr

logger = logging.getLogger(name="receipts")

receipts_api = Blueprint('receipts', __name__)


@receipts_api.route('/api/v1/receipts/qr', methods=['POST'])
@auth()
@jsonbody(event_id=features(type=int, required=True),
          qr=features(type=str, required=True))
def save_receipt(event_id: int, qr: str, create_receipt_by_qr=CreateReceiptByQr()):
    result = formatting(create_receipt_by_qr(user_id=getattr(request, "user_id"),
                                             event_id=event_id,
                                             qr=qr))
    return SuccessResponse(result)
