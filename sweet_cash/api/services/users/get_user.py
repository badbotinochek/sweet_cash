import logging

from api.models.users import UserModel

logger = logging.getLogger(name="auth")


class GetUser:

    def __call__(self, user_id: str) -> UserModel:
        return UserModel.get(user_id=user_id)
