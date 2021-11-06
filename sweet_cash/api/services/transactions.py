import logging

from api.models.transaction_type import TransactionType
from api.models.transaction_category import TransactionCategory
from api.models.transaction import TransactionModel
from config import Config
import api.errors as error

logger = logging.getLogger(name="transactions")


def formatting(t: TransactionModel) -> dict:
    formatted_transaction = {
        "id": t.get_id(),
        "created_at": t.created_at,
        "type": TransactionType.get_name(type_id=t.type),
        "category": TransactionCategory.get_name(category_id=t.category),
        "amount": t.amount,
        "transaction_date": t.transaction_date,
        "private": t.private,
        "description": t.description
    }
    return formatted_transaction


class Transaction:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.transaction_id = kwargs.get("transaction_id")
        self.transactions_type_id = kwargs.get("type_id")
        self.transactions_category_id = kwargs.get("category_id")
        self.amount = kwargs.get("amount")
        self.transaction_date = kwargs.get("transaction_date")
        self.private = kwargs.get("private")
        self.description = kwargs.get("description")
        self.created_at = None

    def create(self) -> dict:
        transactions_type = TransactionType.get(type_id=self.transactions_type_id)
        if transactions_type is None:
            logger.warning(f'User {self.user_id} is trying to create transaction with a non-existent'
                           f'type {self.transactions_type_id}')
            raise error.APIValueNotFound(f'Transaction type with id {self.transactions_type_id} not found')

        transactions_category = TransactionCategory.get(category_id=self.transactions_category_id)
        if transactions_category is None:
            logger.warning(f'User {self.user_id} is trying to create transaction with a non-existent'
                           f'category {self.transactions_category_id}')
            raise error.APIValueNotFound(f'Transaction category with id {self.transactions_category_id} not found')

        if self.amount < Config.MIN_TRANSACTION_AMOUNT or self.amount > Config.MAX_TRANSACTION_AMOUNT:
            logger.warning(f'User {self.user_id} is trying to create transaction with invalid amount {self.amount}')
            raise error.APIParamError(f'Amount must be from {Config.MIN_TRANSACTION_AMOUNT} '
                                      f'to {Config.MAX_TRANSACTION_AMOUNT}')

        transaction = self.create_new_transaction()

        logger.info(f'User {self.user_id} created transaction {self.transaction_id}')

        return formatting(transaction)

    def create_new_transaction(self) -> TransactionModel:
        transaction = TransactionModel(type=self.transactions_type_id,
                                       user_id=self.user_id,
                                       category=self.transactions_category_id,
                                       amount=self.amount,
                                       transaction_date=self.transaction_date,
                                       private=self.private)

        if self.description is not None:
            transaction.description = self.description

        transaction.create()

        logger.info(f'Created new user {self.transaction_id}')

        return transaction

    def update(self) -> dict:
        transaction = TransactionModel.get(transaction_id=self.transaction_id, user_id=int(self.user_id))
        if transaction is None:
            logger.warning(f'User {self.user_id} is trying to update a non-existent transaction {self.transaction_id}')
            raise error.APIValueNotFound(f'Transaction {self.transaction_id} not found')

        transactions_type = TransactionType.get(type_id=self.transactions_type_id)
        if transactions_type is None:
            logger.warning(f'User {self.user_id} is trying to create transaction with a non-existent'
                           f'type {self.transactions_type_id}')
            raise error.APIValueNotFound(f'Transaction type with id {self.transactions_type_id} not found')

        transactions_category = TransactionCategory.get(category_id=self.transactions_category_id)
        if transactions_category is None:
            logger.warning(f'User {self.user_id} is trying to create transaction with a non-existent'
                           f'category {self.transactions_category_id}')
            raise error.APIValueNotFound(f'Transaction category with id {self.transactions_category_id} not found')

        if self.amount < Config.MIN_TRANSACTION_AMOUNT or self.amount > Config.MAX_TRANSACTION_AMOUNT:
            logger.warning(f'User {self.user_id} is trying to create transaction with invalid amount {self.amount}')
            raise error.APIParamError(f'Amount must be from {Config.MIN_TRANSACTION_AMOUNT} '
                                      f'to {Config.MAX_TRANSACTION_AMOUNT}')

        transaction.update(type_id=self.transactions_type_id,
                           category_id=self.transactions_category_id,
                           amount=self.amount,
                           transaction_date=self.transaction_date,
                           private=self.private,
                           description=self.description)

        logger.info(f'User {self.user_id} updated transaction {self.transaction_id}')

        return formatting(transaction)

    def get(self) -> dict:
        transaction = TransactionModel.get(transaction_id=self.transaction_id, user_id=int(self.user_id))
        if transaction is None:
            logger.warning(f'User {self.user_id} is trying to get a non-existent transaction {self.transaction_id}')
            raise error.APIValueNotFound(f'Transaction {self.transaction_id} not found')

        logger.info(f'User {self.user_id} got transaction {self.transaction_id}')

        return formatting(transaction)

    def get_batch(self, limit=100, offset=0) -> list:
        transactions = TransactionModel.get_transactions(user_id=int(self.user_id),
                                                         offset=int(offset),
                                                         limit=int(limit))

        transactions = [formatting(t) for t in transactions]

        logger.info(f'User {self.user_id} got transactions')

        return transactions

    def delete(self):
        transaction = TransactionModel.get(transaction_id=self.transaction_id, user_id=int(self.user_id))
        if transaction is None:
            logger.warning(f'User {self.user_id} is trying to delete a non-existent'
                           f'transaction {self.transaction_id}')
            raise error.APIValueNotFound(f'Transaction {self.transaction_id} not found')

        TransactionModel.delete_transaction(transaction_id=self.transaction_id)

        logger.info(f'User {self.user_id} deleted transaction {self.transaction_id}')
