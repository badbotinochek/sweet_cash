
from flask import request, Blueprint
import logging

from sweet_cash.api.services.nalog_ru.send_otp import SendOtpForNalogRu
from sweet_cash.api.services.nalog_ru.verify_otp import VerifyOtpForNalogRu
from sweet_cash.api.api import SuccessResponse, auth, jsonbody, features

logger = logging.getLogger(name="external_auth")

external_auth_api = Blueprint('external_auth', __name__)


@external_auth_api.route('/api/v1/nalog/otp/send', methods=['POST'])
@auth()
def send_otp(send_otp=SendOtpForNalogRu()):
    return SuccessResponse(send_otp(user_id=getattr(request, "user_id")))


@external_auth_api.route('/api/v1/nalog/otp/verify', methods=['POST'])
@auth()
@jsonbody(otp=features(type=str, required=True))
def verify_otp(otp: str, verify_otp=VerifyOtpForNalogRu()):
    return SuccessResponse(verify_otp(user_id=getattr(request, "user_id"), otp=otp))
