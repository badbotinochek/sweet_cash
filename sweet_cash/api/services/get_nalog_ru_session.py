import logging

from api.models.external_session import NalogRuSessionModel

logger = logging.getLogger(name="auth")


class GetNalogRuSession:

    def __call__(self, user_id) -> NalogRuSessionModel:
        return NalogRuSessionModel.get_by_user(user_id=user_id)
