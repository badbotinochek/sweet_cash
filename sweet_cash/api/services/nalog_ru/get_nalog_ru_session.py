import logging

from api.models.nalog_ru_session import NalogRuSessionModel
import api.errors as error

logger = logging.getLogger(name="nalog_ru")


class GetNalogRuSession:

    def __call__(self, user_id: int) -> NalogRuSessionModel:
        session = NalogRuSessionModel.get_by_user(user_id=user_id)
        return session
