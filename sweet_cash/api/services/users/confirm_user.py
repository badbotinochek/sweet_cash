
import logging
from flask_jwt_extended import decode_token
from pathlib import Path

from api.models.users import UserModel
import api.errors as error

logger = logging.getLogger(name="auth")


class ConfirmUser(object):

    def __call__(self, email: str, confirmation_code: str):

        user = UserModel.get_user(email=email)

        if user is None:
            logger.warning(f'User with email {email} is trying to confirm registration')
            raise error.APIValueNotFound(f'User with email {email} not found')

        try:
            decode_token(encoded_token=confirmation_code)
        except Exception as e:
            return open('sweet_cash/templates/fail_confirmation.html', 'r').read()

        user.update(confirmed=True)

        logger.info(f'User {user.id} confirmed')

        return open('sweet_cash/templates/success_confirmation.html', 'r').read()
