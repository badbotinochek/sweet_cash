import logging

from api.api import check_email_format, check_password_format, check_phone_format
from api.models.users import UserModel
from api.models.session import SessionModel
from api.models.external_session import NalogRuSessionModel
import api.errors as error

logger = logging.getLogger(name="auth")


class User:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.password = kwargs.get("password")
        self.user_id = None
        self.token = None
        self.auth_in_nalog_ru = False

    def register(self):
        if not check_email_format(self.email):
            raise error.APIParamError('Invalid email format')

        if not check_phone_format(self.phone):
            raise error.APIParamError('Invalid phone format')

        if not check_password_format(self.password):
            raise error.APIParamError('Invalid password format')

        user = UserModel.get_user(self.email)

        if user is not None:
            logger.info(f'User tried to register with an already registered email {self.email}')
            raise error.APIConflict('Email already registered')

        self.create_new_user()

        logger.info(f'User {self.user_id} registered with email {self.email}')

    def login(self, login_method: str):
        if not check_email_format(self.email):
            raise error.APIParamError('Invalid email format')

        if not check_password_format(self.password):
            raise error.APIParamError('Invalid password format')

        user = UserModel.get_user(self.email)

        if user is None:
            logger.info(f'User with email {self.email} tried to login')
            raise error.APIValueNotFound('User not registered')

        if not user.check_password(self.password):
            logger.info(f'User {user.get_id()} with email {self.email} try to login with wrong password')
            raise error.APIAuthError('Wrong password')

        self.user_id = user.get_id()

        self.new_token(login_method=login_method)

        # Check auth in NalogRu API for user
        self.check_nalog_ru_auth()

        logger.info(f'User {self.user_id} login with email {self.email}')

        return {
            "access_token": self.token,
            "user_id": self.user_id,
            "auth_in_nalog_ru": self.auth_in_nalog_ru
        }

    def create_new_user(self):
        user = UserModel(name=self.name,
                         email=self.email,
                         phone=self.phone,
                         password=self.password)
        user.create()
        self.user_id = user.get_id()
        logger.info(f'Created new user {self.user_id}')

    def new_token(self, login_method: str):
        session = SessionModel.get(user_id=self.user_id)

        if session is not None:
            session.update(login_method=login_method)
        else:
            session = SessionModel(user_id=self.user_id, login_method=login_method)
            session.create()

        self.token = session.get_token()

    def check_nalog_ru_auth(self):
        nalog_ru_session = NalogRuSessionModel.get_by_user(user_id=self.user_id)
        if nalog_ru_session is not None:
            self.auth_in_nalog_ru = True
