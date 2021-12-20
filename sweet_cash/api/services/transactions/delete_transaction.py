import logging

from api.models.transaction import TransactionModel

logger = logging.getLogger(name="transactions")


class DeleteTransaction:

    def __call__(self, user_id: int, transaction_id: int) -> int:
        num_transaction_deleted = TransactionModel.delete_transaction(transaction_id=transaction_id,
                                                                      user_id=user_id)

        logger.info(f'User {user_id} deleted transaction {transaction_id}')

        return num_transaction_deleted
