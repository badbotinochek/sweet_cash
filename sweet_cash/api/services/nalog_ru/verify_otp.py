import logging

from sweet_cash.api.api import check_phone_format
from sweet_cash.api.services.users.get_user import GetUser
from sweet_cash.api.services.nalog_ru.create_or_update_nalog_ru_session import CreateOrUpdateNalogRuSession
from sweet_cash.api.integrations.nalog_ru import NalogRuApi
import sweet_cash.api.errors as error

logger = logging.getLogger(name="nalog_ru")


class VerifyOtpForNalogRu(object):
    get_user = GetUser()
    nalog_ru_api = NalogRuApi()
    create_or_update_nalog_ru_session = CreateOrUpdateNalogRuSession()

    def __call__(self, user_id: int, otp: str):

        user = self.get_user(user_id=user_id)

        phone = user.phone

        if not check_phone_format(phone):
            raise error.APIError('Invalid phone format')

        session_id, refresh_token = self.nalog_ru_api.verify_otp(phone=phone, otp=otp)

        self.create_or_update_nalog_ru_session(user_id=user_id,
                                               session_id=session_id,
                                               refresh_token=refresh_token)

        logger.info(f'User {user_id} verified otp for phone {phone}')

        return "Ok"
