import logging

from api.api import check_email_format, check_password_format
from api.models.users import UserModel
from api.models.session import SessionModel
from api.services.nalog_ru_session import NalogRuSession
import api.errors as error

logger = logging.getLogger(name="auth")


class LoginUser:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.login_method = kwargs.get("login_method")
        self.auth_in_nalog_ru = False
        self.token = None

    def __call__(self):
        if not check_email_format(self.email):
            raise error.APIParamError('Invalid email format')

        if not check_password_format(self.password):
            raise error.APIParamError('Invalid password format')

        user = UserModel.get_user(self.email)

        if user is None:
            logger.info(f'User with email {self.email} tried to login')
            raise error.APIValueNotFound('User not registered')

        if not user.check_password(self.password):
            logger.info(f'User with email {self.email} try to login with wrong password')
            raise error.APIAuthError('Wrong password')

        self.user_id = user.id

        self._new_token()

        # Check auth in NalogRu API for user
        self._check_nalog_ru_auth()

        logger.info(f'User {self.user_id} login with email {self.email}')

        return {
            "access_token": self.token,
            "user_id": self.user_id,
            "auth_in_nalog_ru": self.auth_in_nalog_ru
        }

    def _new_token(self):
        session = SessionModel.get(user_id=self.user_id)

        if session is not None:
            session.update(login_method=self.login_method)
        else:
            session = SessionModel(user_id=self.user_id, login_method=self.login_method)
            session.create()

        self.token = session.token

    def _check_nalog_ru_auth(self):
        nalog_ru_session = NalogRuSession(user_id=self.user_id).get()
        if nalog_ru_session is not None:
            self.auth_in_nalog_ru = True
