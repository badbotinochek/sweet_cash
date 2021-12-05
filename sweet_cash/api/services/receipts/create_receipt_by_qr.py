from datetime import datetime
import logging

from api.integrations.nalog_ru import NalogRuApi
from api.models.receipt import ReceiptModel
from api.services.transactions.create_or_update_transaction import CreateOrUpdateTransaction
import api.errors as error

logger = logging.getLogger(name="receipts")


def convert_to_utc(ts: int):
    utc_dt = datetime.utcfromtimestamp(ts)
    return utc_dt.isoformat()


class CreateReceiptByQr:

    def __call__(self, user_id, qr) -> ReceiptModel:
        self.user_id = user_id
        self.receipt_id, self.receipt_data = nalog_ru_api.get_ticket(user_id=user_id, qr=qr)

        receipt = ReceiptModel.get_by_user(receipt_id=self.receipt_id, user_id=user_id)

        if receipt is not None:
            logger.warning(f'User {user_id} is trying to save a saved receipt')
            raise error.APIConflict('Receipt has already been saved')

        receipt = ReceiptModel(user_id=user_id,
                               external_id=self.receipt_id,
                               data=self.receipt_data)

        transaction = self._save_transaction_by_receipt()

        if transaction is not None:
            receipt.transaction_id = transaction.id

        receipt.create()

        logger.info(f'User {user_id} save receipt {self.receipt_id}')

        return receipt

    def _save_transaction_by_receipt(self, create_or_update_transaction=CreateOrUpdateTransaction()):
        if "operation" not in self.receipt_data and "dateTime" not in self.receipt_data:
            logger.error(f'Error saving transaction for receipt {self.receipt_id} with receipt '
                         f'data {self.receipt_data}')
            return None

        amount = self.receipt_data["operation"]["sum"] / 100
        transaction_date = convert_to_utc(self.receipt_data["ticket"]["document"]["receipt"]["dateTime"])
        type = "Income"
        category_id = 1  # TODO Искать категорию по наименованию

        transaction = create_or_update_transaction(user_id=self.user_id,
                                                   type=type,
                                                   category_id=category_id,
                                                   amount=amount,
                                                   transaction_date=transaction_date)

        logger.info(f'User {self.user_id} create new transaction by receipt {self.receipt_id}')

        return transaction


nalog_ru_api = NalogRuApi()
