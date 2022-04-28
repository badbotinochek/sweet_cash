import logging

from sweet_cash.api.api import check_phone_format
from sweet_cash.api.services.users.get_user import GetUser
from sweet_cash.api.integrations.nalog_ru import NalogRuApi
import sweet_cash.api.errors as error

logger = logging.getLogger(name="nalog_ru")


class SendOtpForNalogRu(object):
    nalog_ru_api = NalogRuApi()
    get_user = GetUser()

    def __call__(self, user_id: int):
        user = self.get_user(user_id=user_id)

        phone = user.phone

        if not check_phone_format(phone):
            raise error.APIParamError('Invalid phone format')

        self.nalog_ru_api.send_otp_sms(phone=phone)

        logger.info(f'User {user_id} is trying to send otp SMS')

        return "Ok"
