import logging

from api.models.receipt import ReceiptModel
import api.errors as error

logger = logging.getLogger(name="transactions")


class GetReceipt:

    def __call__(self, user_id: int, receipt_id: int) -> ReceiptModel:
        receipt = ReceiptModel.get_by_user(receipt_id=receipt_id, user_id=int(user_id))
        if receipt is None:
            logger.warning(f'User {user_id} is trying to get a non-existent receipt {receipt_id}')
            raise error.APIValueNotFound(f'Receipt with id {receipt_id} not found for user {user_id}')

        logger.info(f'User {user_id} got receipt {receipt_id}')

        return receipt
