import logging

from sweet_cash.api.models.users import UserModel
import sweet_cash.api.errors as error

logger = logging.getLogger(name="auth")


class GetUser(object):

    def __call__(self, user_id: int) -> UserModel:

        user = UserModel.get(user_id=user_id)

        if user is None:
            logger.warning(f'User with id {user_id} not found')
            raise error.APIValueNotFound(f'User {user_id} not found')

        return user
