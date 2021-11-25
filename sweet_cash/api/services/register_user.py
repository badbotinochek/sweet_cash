import logging

from api.api import check_email_format, check_password_format, check_phone_format
from api.models.users import UserModel
import api.errors as error

logger = logging.getLogger(name="auth")


class RegisterUser:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.password = kwargs.get("password")

    def __call__(self):
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

        self._create_new_user()

        logger.info(f'User {self.user_id} registered with email {self.email}')

        return "Ok"

    def _create_new_user(self):
        user = UserModel(name=self.name,
                         email=self.email,
                         phone=self.phone,
                         password=self.password)
        user.create()
        self.user_id = user.id
        logger.info(f'Created new user {self.user_id}')
