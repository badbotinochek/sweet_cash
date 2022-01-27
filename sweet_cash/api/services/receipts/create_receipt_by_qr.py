from datetime import datetime
import logging

from api.integrations.nalog_ru import NalogRuApi
from api.models.receipt import ReceiptModel
from api.services.transactions.create_or_update_transaction import CreateOrUpdateTransaction
from api.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession
import api.errors as error

logger = logging.getLogger(name="receipts")


def convert_to_utc(ts: int):
    utc_dt = datetime.utcfromtimestamp(ts)
    return utc_dt.isoformat()


class CreateReceiptByQr:
    nalog_ru_api = NalogRuApi()
    get_nalog_ru_session = GetNalogRuSession()

    def __call__(self, user_id: int, qr) -> ReceiptModel:
        # Get nalog ru session
        session = self.get_nalog_ru_session(user_id=user_id)

        if session is None:
            logger.warning(f'User {user_id} is trying to get a non-existent nalog ru session')
            raise error.APIAuthError('User is not authorized in NalogRu Api')

        logger.info(f'User {user_id} got nalog ru session')

        # Get receipt data
        receipt_id, receipt_data = self.nalog_ru_api.get_ticket(user_id=user_id,
                                                                session_id=session.session_id,
                                                                refresh_token=session.refresh_token,
                                                                qr=qr)

        logger.info(f'Got receipt {receipt_id} for user {user_id}')

        # Save receipt
        receipt = ReceiptModel.get_by_external_id(external_id=receipt_id, user_id=user_id)

        if receipt is not None:
            logger.warning(f'User {user_id} is trying to save a saved receipt')
            raise error.APIConflict('Receipt has already been saved')

        receipt = ReceiptModel(user_id=user_id,
                               external_id=receipt_id,
                               data=receipt_data)

        transaction = self._save_transaction_by_receipt(user_id=user_id,
                                                        receipt_id=receipt_id,
                                                        receipt_data=receipt_data)

        if transaction is not None:
            receipt.transaction_id = transaction.id

        receipt.create()

        logger.info(f'User {user_id} save receipt {receipt_id}')

        return receipt

    def _save_transaction_by_receipt(self, user_id: int,
                                     receipt_id: str,
                                     receipt_data: dict,
                                     create_or_update_transaction=CreateOrUpdateTransaction()):
        if "operation" not in receipt_data and "dateTime" not in receipt_data:
            logger.error(f'Error saving transaction for receipt {receipt_id} with receipt '
                         f'data {receipt_data}')
            return None

        amount = receipt_data["operation"]["sum"] / 100
        transaction_date = convert_to_utc(receipt_data["ticket"]["document"]["receipt"]["dateTime"])
        type = "Income"
        category_id = 1  # TODO Искать категорию по наименованию

        transaction = create_or_update_transaction(user_id=user_id,
                                                   type=type,
                                                   category_id=category_id,
                                                   amount=amount,
                                                   transaction_date=transaction_date)

        logger.info(f'User {user_id} create new transaction by receipt {receipt_id}')

        return transaction
