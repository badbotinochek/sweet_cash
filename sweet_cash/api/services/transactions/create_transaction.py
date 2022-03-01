import logging

from api.models.transaction_category import TransactionCategoryModel
from api.services.events.get_event_participant import GetEventParticipant
from api.services.receipts.get_receipt import GetReceipt
from api.models.transaction import TransactionModel, TransactionType
from config import Config
import api.errors as error

logger = logging.getLogger(name="transactions")


class CreateTransaction:
    event_participant = GetEventParticipant()
    receipt = GetReceipt()

    def __call__(self, **kwargs) -> TransactionModel:
        user_id = kwargs.get("user_id")
        event_id = kwargs.get("event_id")
        transaction_date = kwargs.get("transaction_date")
        transactions_type = kwargs.get("type")
        transactions_category_id = kwargs.get("category_id")
        amount = kwargs.get("amount")
        receipt_id = kwargs.get("receipt_id")
        description = kwargs.get("description")

        if amount < Config.MIN_TRANSACTION_AMOUNT or amount > Config.MAX_TRANSACTION_AMOUNT:
            logger.warning(f'User {user_id} is trying to create transaction with invalid amount {amount}')
            raise error.APIParamError(f'Amount must be from {Config.MIN_TRANSACTION_AMOUNT} '
                                      f'to {Config.MAX_TRANSACTION_AMOUNT}')

        if not TransactionType.has_value(transactions_type):
            logger.warning(f'User {user_id} is trying to create transaction with invalid '
                           f'type {transactions_type}')
            raise error.APIParamError(f'Invalid transaction type {transactions_type}')

        # TODO Проверять категорию через сервис
        transactions_category = TransactionCategoryModel.get_by_id(category_id=transactions_category_id)
        if transactions_category is None:
            logger.warning(f'User {user_id} is trying to create transaction with a non-existent'
                           f'category {transactions_category_id}')
            raise error.APIValueNotFound(f'Transaction category with id {transactions_category_id} not found')

        self.event_participant(event_id=event_id, user_id=user_id, accepted=True)

        if receipt_id is not None:
            self.receipt(receipt_id=receipt_id, user_id=user_id)

        transaction = TransactionModel(user_id=user_id,
                                       event_id=event_id,
                                       transaction_date=transaction_date,
                                       type=TransactionType(transactions_type),
                                       category=transactions_category_id,
                                       amount=amount,
                                       receipt_id=receipt_id,
                                       description=description)

        transaction.create()

        logger.info(f'User {user_id} created transaction {transaction.id}')

        return transaction
