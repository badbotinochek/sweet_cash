import logging

from api.models.transaction_category import TransactionCategory
from api.services.events.get_event_user import GetEventUser
from api.services.receipts.get_receipt import GetReceipt
from api.models.transaction import TransactionModel, TransactionType
from config import Config
import api.errors as error

logger = logging.getLogger(name="transactions")


class CreateOrUpdateTransaction:
    event_user = GetEventUser()
    receipt = GetReceipt()

    def __call__(self, **kwargs) -> TransactionModel:
        transaction_id = kwargs.get("transaction_id")
        number = kwargs.get("number")
        event_id = kwargs.get("event_id")
        user_id = kwargs.get("user_id")
        transactions_type = kwargs.get("type")
        transactions_category_id = kwargs.get("category_id")
        amount = kwargs.get("amount")
        transaction_date = kwargs.get("transaction_date")
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
        transactions_category = TransactionCategory.get(category_id=transactions_category_id)
        if transactions_category is None:
            logger.warning(f'User {user_id} is trying to create transaction with a non-existent'
                           f'category {transactions_category_id}')
            raise error.APIValueNotFound(f'Transaction category with id {transactions_category_id} not found')

        self.event_user(event_id=event_id, user_id=user_id)

        if receipt_id is not None:
            self.receipt(receipt_id=receipt_id, user_id=user_id)

        if transaction_id is not None:

            transaction = TransactionModel.get_by_user(transaction_id=transaction_id, user_id=int(user_id))

            if transaction is None:
                logger.warning(f'User {user_id} is trying to update a non-existent transaction {transaction_id}')
                raise error.APIValueNotFound(f'Transaction {transaction_id} not found')

            transaction.update(number=number,
                               event_id=event_id,
                               type=TransactionType(transactions_type),
                               category_id=transactions_category_id,
                               amount=amount,
                               transaction_date=transaction_date,
                               receipt_id=receipt_id,
                               description=description)

            logger.info(f'User {user_id} updated transaction {transaction_id}')

            return transaction

        transaction = TransactionModel(number=number,
                                       event_id=event_id,
                                       user_id=user_id,
                                       type=TransactionType(transactions_type),
                                       category=transactions_category_id,
                                       amount=amount,
                                       transaction_date=transaction_date,
                                       description=description,
                                       receipt_id=receipt_id)

        if description is not None:
            transaction.description = description

        transaction.create()

        logger.info(f'User {user_id} created transaction {transaction_id}')

        return transaction
