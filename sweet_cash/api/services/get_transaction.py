import logging

from api.models.transaction import TransactionModel
import api.errors as error

logger = logging.getLogger(name="transactions")


class GetTransaction:

    def __call__(self, user_id, transaction_id) -> TransactionModel:
        transaction = TransactionModel.get(transaction_id=transaction_id, user_id=int(user_id))
        if transaction is None:
            logger.warning(f'User {user_id} is trying to get a non-existent transaction {transaction_id}')
            raise error.APIValueNotFound(f'Transaction {transaction_id} not found')

        logger.info(f'User {user_id} got transaction {transaction_id}')

        return transaction
