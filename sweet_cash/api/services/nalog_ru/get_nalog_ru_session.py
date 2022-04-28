import logging

from sweet_cash.api.models.nalog_ru_session import NalogRuSessionModel


logger = logging.getLogger(name="nalog_ru")


class GetNalogRuSession(object):

    def __call__(self, user_id: int) -> NalogRuSessionModel:
        session = NalogRuSessionModel.get_by_user(user_id=user_id)
        return session
