import logging

from api.models.transaction import TransactionModel
from api.models.event_participants import EventParticipantRole
from api.services.transactions.get_transaction import GetTransactions
from api.services.events.get_event_participant import GetEventParticipant
import api.errors as error

logger = logging.getLogger(name="transactions")


class DeleteTransaction:
    get_transactions = GetTransactions()
    event_participant = GetEventParticipant()

    def __call__(self, user_id: int, transaction_id: int) -> int:
        # Get transaction
        transaction = self.get_transactions(user_id=user_id, transaction_ids=[transaction_id])[0]

        if transaction.user_id != user_id:
            # Checking that user is a participant in event
            participant = self.event_participant(event_id=transaction.event_id, user_id=user_id, accepted=True)
            if participant.role != EventParticipantRole.MANAGER:
                logger.warning(f'User {user_id} is trying to update a unavailable transaction {transaction_id}')
                raise error.APIConflict(f'Deleting a transaction {transaction_id} unavailable for user {user_id}')

        transaction_deleted_num = TransactionModel.delete_transaction(transaction_id=transaction_id)

        if transaction_deleted_num > 0:
            logger.info(f'User {user_id} deleted transaction {transaction_id}')

        return transaction_deleted_num
