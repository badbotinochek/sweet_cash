import logging

from api.models.transaction import TransactionModel, TransactionType
from api.models.transaction_category import TransactionCategoryModel
from api.models.event_participants import EventParticipantRole
from api.services.transactions.get_transaction import GetTransactions
from api.services.events.get_event_participant import GetEventParticipant
from api.services.receipts.get_receipt import GetReceipt
import api.errors as error
from config import Config


logger = logging.getLogger(name="events")


class UpdateTransaction(object):
    get_transactions = GetTransactions()
    get_event_participant = GetEventParticipant()
    get_receipt = GetReceipt()

    def __call__(self, **kwargs) -> TransactionModel:
        user_id = kwargs.get("user_id")
        transaction_id = kwargs.get("transaction_id")
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

        if receipt_id is not None:
            self.get_receipt(receipt_id=receipt_id, user_id=user_id)

        # Get transaction
        transaction = self.get_transactions(user_id=user_id, transaction_ids=[transaction_id])[0]

        if transaction.user_id != user_id:
            # Checking that user is a participant in event
            participant = self.get_event_participant(event_id=transaction.event_id, user_id=user_id, accepted=True)
            if participant.role != EventParticipantRole.MANAGER:
                logger.warning(f'User {user_id} is trying to update a unavailable transaction {transaction_id}')
                raise error.APIConflict(f'Updating a transaction {transaction_id} unavailable for user {user_id}')

        transaction.update(transaction_date=transaction_date,
                           type=TransactionType(transactions_type),
                           category=transactions_category_id,
                           amount=amount,
                           receipt_id=receipt_id,
                           description=description)

        logger.info(f'User {user_id} updated transaction {transaction.id}')

        return transaction
