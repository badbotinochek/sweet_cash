
from datetime import datetime
import logging

from api.integrations.nalog_ru import NalogRuApi
from api.services.transactions import Transaction
from api.models.receipt import ReceiptModel
import api.errors as error


logger = logging.getLogger(name="receipts")


def formatting(r: ReceiptModel) -> dict:
    formatted_receipt = {
        "id": r.id,
        "created_at": r.created_at,
        "external_id": r.external_id,
        "transaction_id": r.transaction_id
    }
    return formatted_receipt


def convert_to_utc(ts: int):
    utc_dt = datetime.utcfromtimestamp(ts)
    return utc_dt.isoformat()


class Receipt:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.qr = kwargs.get("qr")
        self.transaction_id = kwargs.get("transaction_id")
        self.receipt_id = None
        self.receipt_data = None

    def create(self):
        self.receipt_id, self.receipt_data = nalog_ru_api.get_ticket(user_id=self.user_id, qr=self.qr)

        receipt = ReceiptModel.get_by_user(receipt_id=self.receipt_id, user_id=self.user_id)

        if receipt is not None:
            logger.warning(f'User {self.user_id} is trying to save a saved receipt')
            raise error.APIConflict('Receipt has already been saved')

        receipt = ReceiptModel(user_id=self.user_id,
                               external_id=self.receipt_id,
                               data=self.receipt_data)

        transaction = self.save_transaction_by_receipt()

        if transaction is not None:
            receipt.transaction_id = transaction["id"]

        receipt.create()

        logger.info(f'User {self.user_id} save receipt {self.receipt_id}')

        return formatting(receipt)

    def save_transaction_by_receipt(self):
        if "operation" not in self.receipt_data and "dateTime" not in self.receipt_data:
            logger.error(f'Error saving transaction for receipt {self.receipt_id} with receipt '
                         f'data {self.receipt_data}')
            return None

        amount = self.receipt_data["operation"]["sum"] / 100
        transaction_date = convert_to_utc(self.receipt_data["ticket"]["document"]["receipt"]["dateTime"])
        type_id = 1  # TODO Подставлять тип дохода
        category_id = 1  # TODO Искать категорию по наименованию

        transaction = Transaction(user_id=self.user_id,
                                  type_id=type_id,
                                  category_id=category_id,
                                  amount=amount,
                                  transaction_date=transaction_date).create()

        logger.info(f'User {self.user_id} create new transaction by receipt {self.receipt_id}')

        return transaction


nalog_ru_api = NalogRuApi()
