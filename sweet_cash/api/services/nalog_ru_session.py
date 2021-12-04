import logging

from api.models.nalog_ru_session import NalogRuSessionModel

logger = logging.getLogger(name="auth")


class NalogRuSession:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
        self.refresh_token = kwargs.get("refresh_token")

    def get(self) -> NalogRuSessionModel:
        return NalogRuSessionModel.get_by_user(user_id=self.user_id)

    def create(self) -> dict:
        session = NalogRuSessionModel(user_id=self.user_id,
                                      session_id=self.session_id,
                                      refresh_token=self.refresh_token)

        session.create()

        logger.info(f'Created new NalogRuSession for user {self.user_id}')

        return session

    def update(self):
        session = NalogRuSessionModel.get_by_user(user_id=int(self.user_id))
        if session is None:
            logger.warning(f'User {self.user_id} is trying to update a non-existent NalogRu session')
            session = self.create()
            return session

        session.update(session_id=self.session_id,
                       refresh_token=self.refresh_token)

        logger.info(f'Updated NalogRuSession for user {self.user_id}')

        return session
