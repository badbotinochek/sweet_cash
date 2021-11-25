import logging

from api.models.transaction import TransactionModel

logger = logging.getLogger(name="transactions")


class GetTransactions:

    def __call__(self, user_id, limit=100, offset=0) -> [TransactionModel]:
        transactions = TransactionModel.get_transactions(user_id=int(user_id),
                                                         offset=int(offset),
                                                         limit=int(limit))

        transactions = [t for t in transactions]

        logger.info(f'User {user_id} got transactions')

        return transactions
