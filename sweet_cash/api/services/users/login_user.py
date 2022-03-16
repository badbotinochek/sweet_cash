import logging

from sweet_cash.api.api import check_email_format, check_password_format
from sweet_cash.api.models.users import UserModel
from sweet_cash.api.models.session import SessionModel
from sweet_cash.api.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession

import sweet_cash.api.errors as error

logger = logging.getLogger(name="auth")


class LoginUser(object):

    def __call__(self, email: str, password: str, login_method: str) -> dict:
        if not check_email_format(email):
            raise error.APIParamError('Invalid email format')

        if not check_password_format(password):
            raise error.APIParamError('Invalid password format')

        user = UserModel.get_user(email)

        if user is None:
            logger.info(f'User with email {email} tried to login')
            raise error.APIValueNotFound('User not registered')

        if not user.check_password(password):
            logger.info(f'User with email {email} try to login with wrong password')
            raise error.APIAuthError('Wrong password')

        self.user_id = user.id

        self._update_session(login_method)

        logger.info(f'User {self.user_id} login with email {email}')

        return {
            "refresh_token": self.refresh_token,
            "user_id": self.user_id,
            "auth_in_nalog_ru": self._check_nalog_ru_auth()
        }

    def _update_session(self, login_method):
        session = SessionModel.get(user_id=self.user_id)

        if session is not None:
            session.update(login_method=login_method)
        else:
            session = SessionModel(user_id=self.user_id, login_method=login_method)
            session.create()

        self.refresh_token = session.refresh_token

    # Check auth in NalogRu API for user
    def _check_nalog_ru_auth(self, get_nalog_ru_session=GetNalogRuSession()):
        nalog_ru_session = get_nalog_ru_session(user_id=self.user_id)
        if nalog_ru_session is not None:
            return True
        return False
