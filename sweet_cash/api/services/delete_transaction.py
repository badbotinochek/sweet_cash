import logging

from api.models.transaction import TransactionModel

logger = logging.getLogger(name="transactions")


class DeleteTransaction:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.transaction_id = kwargs.get("transaction_id")

    def __call__(self) -> int:
        num_transaction_deleted = TransactionModel.delete_transaction(transaction_id=self.transaction_id,
                                                                      user_id=self.user_id)

        logger.info(f'User {self.user_id} deleted transaction {self.transaction_id}')

        return num_transaction_deleted
