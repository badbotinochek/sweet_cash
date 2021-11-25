import logging

from api.models.transaction import TransactionModel

logger = logging.getLogger(name="transactions")


class GetTransactions:

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")

    def __call__(self, limit=100, offset=0) -> [TransactionModel]:
        transactions = TransactionModel.get_transactions(user_id=int(self.user_id),
                                                         offset=int(offset),
                                                         limit=int(limit))

        transactions = [t for t in transactions]

        logger.info(f'User {self.user_id} got transactions')

        return transactions
