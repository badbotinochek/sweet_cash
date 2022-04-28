import logging

from sweet_cash.api.models.transaction import TransactionModel
from sweet_cash.api.services.events.get_event_participant import GetEventParticipant
from sweet_cash.api.api import str2datetime
import sweet_cash.api.errors as error

logger = logging.getLogger(name="transactions")


class GetAllTransactions(object):
    get_event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> [TransactionModel]:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        start = kwargs.get("start")
        end = kwargs.get("end")
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")

        if start is not None and end is not None:
            if str2datetime(start) > str2datetime(end):
                raise error.APIParamError(f'Start {start} must be less than End {end}')

        # Checking that user is the event manager
        participant = self.get_event_participant(event_id=event_id, user_id=user_id, accepted=True)

        if participant.role == 'Partner':
            transactions = TransactionModel.get_transactions_by_user_id(user_id=user_id,
                                                                        start=start,
                                                                        end=end,
                                                                        limit=int(limit),
                                                                        offset=int(offset))
        else:
            transactions = TransactionModel.get_transactions_by_event_id(event_id=event_id,
                                                                         start=start,
                                                                         end=end,
                                                                         limit=int(limit),
                                                                         offset=int(offset))

        transactions = [t for t in transactions]

        logger.info(f'User {user_id} got transactions')

        return transactions
