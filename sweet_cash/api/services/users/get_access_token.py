import logging

from api.models.session import SessionModel
import api.errors as error

logger = logging.getLogger(name="auth")


class GetAccessToken(object):

    def __call__(self, refresh_token: str) -> dict:
        session = SessionModel.get(refresh_token=refresh_token)

        if session is None:
            logger.info(f'Try getting non-existing session by refresh token {refresh_token}')
            raise error.APIValueNotFound(f'Token not found')

        session.update()

        logger.info(f'User with id {session.user_id} got new token')

        return {
            "refresh_token": session.refresh_token,
            "token": session.token
        }
