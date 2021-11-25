import logging

from api.models.external_session import NalogRuSessionModel

logger = logging.getLogger(name="auth")


class CreateOrUpdateNalogRuSession:

    def __call__(self, user_id, session_id, refresh_token) -> NalogRuSessionModel:
        session = NalogRuSessionModel.get_by_user(user_id=int(user_id))
        if session is None:
            session = NalogRuSessionModel(user_id=user_id,
                                          session_id=session_id,
                                          refresh_token=refresh_token)

            session.create()

            logger.info(f'Created new NalogRuSession for user {user_id}')

        session.update(session_id=session_id,
                       refresh_token=refresh_token)

        logger.info(f'Updated NalogRuSession for user {user_id}')

        return session
