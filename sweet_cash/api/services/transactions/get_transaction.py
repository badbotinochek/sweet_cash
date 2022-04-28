import logging

from sweet_cash.api.models.transaction import TransactionModel
from sweet_cash.api.models.event_participants import EventParticipantRole
from sweet_cash.api.services.events.get_event_participant import GetEventParticipant
from sweet_cash.api.api import ids2list
import sweet_cash.api.errors as error

logger = logging.getLogger(name="transactions")


class GetTransactions(object):
    get_event_participant = GetEventParticipant()

    def __call__(self, **kwargs) -> [TransactionModel]:
        user_id = kwargs.get("user_id")
        transaction_ids = ids2list(kwargs.get("transaction_ids"))

        transactions = []
        for transaction_id in transaction_ids:

            transaction = TransactionModel.get_by_id(transaction_id=transaction_id)

            if transaction is None:
                logger.warning(f'User {user_id} is trying to get a non-existent transaction {transaction_id}')
                raise error.APIValueNotFound(f'Transaction {transaction_id} not found for user {user_id}')

            if transaction.user_id != user_id:
                # Checking that user is a participant in event
                participant = self.get_event_participant(event_id=transaction.event_id, user_id=user_id, accepted=True)
                if participant.role == EventParticipantRole.PARTNER:
                    logger.warning(f'User {user_id} is trying to get a unavailable transaction {transaction_id}')
                    raise error.APIConflict(f'Transaction {transaction_id} unavailable for user {user_id}')

            transactions.append(transaction)

        logger.info(f'User {user_id} got transactions')

        return transactions
