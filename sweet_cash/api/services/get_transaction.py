import logging

from api.models.transaction import TransactionModel
import api.errors as error

logger = logging.getLogger(name="transactions")


class GetTransaction:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.transaction_id = kwargs.get("transaction_id")

    def __call__(self) -> TransactionModel:
        transaction = TransactionModel.get(transaction_id=self.transaction_id, user_id=int(self.user_id))
        if transaction is None:
            logger.warning(f'User {self.user_id} is trying to get a non-existent transaction {self.transaction_id}')
            raise error.APIValueNotFound(f'Transaction {self.transaction_id} not found')

        logger.info(f'User {self.user_id} got transaction {self.transaction_id}')

        return transaction
