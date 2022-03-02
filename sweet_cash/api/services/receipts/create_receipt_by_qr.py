from datetime import datetime
import logging

from api.integrations.nalog_ru import NalogRuApi
from api.models.receipt import ReceiptModel
from api.services.transactions.create_transaction import CreateTransaction
from api.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession
from api.services.events.get_event_participant import GetEventParticipant
import api.errors as error

logger = logging.getLogger(name="receipts")


def convert_to_utc(ts: int):
    utc_dt = datetime.utcfromtimestamp(ts)
    return utc_dt.isoformat()


class CreateReceiptByQr(object):
    nalog_ru_api = NalogRuApi()
    get_nalog_ru_session = GetNalogRuSession()
    get_event_participant = GetEventParticipant()
    create_transaction = CreateTransaction()

    def __call__(self, **kwargs) -> ReceiptModel:
        # Get nalog ru session
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        qr = kwargs.get("qr")

        session = self.get_nalog_ru_session(user_id=user_id)

        if session is None:
            logger.warning(f'User {user_id} is trying to get a non-existent nalog ru session')
            raise error.APIAuthError('User is not authorized in NalogRu Api')

        logger.info(f'User {user_id} got nalog ru session')

        self.get_event_participant(user_id=user_id, event_id=event_id, accepted=True)

        # Get receipt data
        receipt_external_id, receipt_data = self.nalog_ru_api.get_ticket(user_id=user_id,
                                                                         session_id=session.session_id,
                                                                         refresh_token=session.refresh_token,
                                                                         qr=qr)

        logger.info(f'Got receipt {receipt_external_id} for user {user_id}')

        # Save receipt
        receipt = ReceiptModel.get_by_external_id(external_id=receipt_external_id, user_id=user_id)

        if receipt is not None:
            logger.warning(f'User {user_id} is trying to save a saved receipt')
            raise error.APIConflict('Receipt has already been saved')

        receipt = ReceiptModel(user_id=user_id,
                               external_id=receipt_external_id,
                               data=receipt_data)

        receipt.create()

        self._save_transaction_by_receipt(user_id=user_id,
                                          event_id=event_id,
                                          receipt_id=receipt.id,
                                          receipt_data=receipt_data)

        logger.info(f'User {user_id} save receipt {receipt.id}')

        return receipt

    def _save_transaction_by_receipt(self, user_id: int,
                                     event_id: int,
                                     receipt_id: str,
                                     receipt_data: dict):
        if "operation" not in receipt_data and "dateTime" not in receipt_data:
            logger.error(f'Error saving transaction for receipt {receipt_id} with receipt '
                         f'data {receipt_data}')
            return None

        amount = receipt_data["operation"]["sum"] / 100
        transaction_date = convert_to_utc(receipt_data["ticket"]["document"]["receipt"]["dateTime"])
        type = "Income"
        category_id = 1  # TODO Искать категорию по наименованию

        transaction = self.create_transaction(user_id=user_id,
                                              event_id=event_id,
                                              transaction_date=transaction_date,
                                              type=type,
                                              category_id=category_id,
                                              amount=amount,
                                              receipt_id=receipt_id)

        logger.info(f'User {user_id} create new transaction by receipt {receipt_id}')

        return transaction
