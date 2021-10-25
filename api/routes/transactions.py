
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
import logging

from api.validator import jsonbody, query_params
from api.models.session import Session
from api.models.transaction import Transaction
from api.models.transaction_type import TransactionType
from api.models.transaction_category import TransactionCategory
from db import db
import api.errors as error

logger = logging.getLogger(name="transactions")

transactions_api = Blueprint('transactions', __name__)


def formatting(t: Transaction) -> dict:
    formatted_transaction = {
        "id": t.id,
        "created_at": t.created_at,
        "type": TransactionType.get_name(type_id=t.type),
        "category": TransactionCategory.get_name(category_id=t.category),
        "amount": t.amount,
        "transaction_date": t.transaction_date,
        "description": t.description
    }
    return formatted_transaction


@transactions_api.route('/api/v1/transaction', methods=['POST'])
@jwt_required()
@jsonbody(type=(int, "required"),
          category=(int, "required"),
          amount=(float, "required"),
          transaction_date=(str, "required"),
          description=(str, None))
def create_transactions(type: int,
                        category: int,
                        amount: float,
                        transaction_date: str,
                        description=''):
    """Create new user transaction

        Returns 401 if

        Returns structure like
        {
            "amount": 2.05,
            "category": "Категория 3",
            "created_at": "Mon, 18 Oct 2021 16:28:33 GMT",
            "description": "description",
            "id": 12,
            "transaction_date": "Sun, 10 Oct 2021 04:25:03 GMT",
            "type": "Тип 3"
        }

        or code 404 if
        {
        }

    """
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction without valid token')
        raise error.APIAuthError('User is not authorized')

    transactions_type = TransactionType.get(type_id=type)
    if transactions_type is None:
        logger.warning(f'User {user_id} is trying to create transaction with a non-existent type {type}')
        raise error.APIValueNotFound(f'Transaction type with id {type} not found')

    transactions_category = TransactionCategory.get(category_id=category)
    if transactions_category is None:
        logger.warning(f'User {user_id} is trying to create transaction with a non-existent category {category}')
        raise error.APIValueNotFound(f'Transaction category with id {category} not found')

    if amount < 0 or amount > 999999999999:
        logger.warning(f'User {user_id} is trying to create transaction with invalid amount {amount}')
        raise error.APIParamError(f'Amount must be from 0 to 999 999 999 999')

    t = Transaction(type=type,
                    user_id=user_id,
                    category=category,
                    amount=amount,
                    transaction_date=transaction_date,
                    description=description)
    db.session.add(t)
    db.session.commit()

    logger.info(f'User {user_id} created transaction {t.get_id()}')

    return jsonify(formatting(t)), 200


@transactions_api.route('/api/v1/transactions', methods=['GET'])
@jwt_required()
@query_params(limit=(str, None),
              offset=(str, None))
def get_transactions(limit=100, offset=0):

    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to get all transactions without valid token')
        raise error.APIAuthError('User is not registered')

    transactions = Transaction.get_transactions(user_id=int(user_id),
                                                offset=int(offset),
                                                limit=int(limit))

    transactions = [formatting(t) for t in transactions]

    logger.info(f'User {user_id} got transactions')

    return jsonify(transactions), 200


@transactions_api.route('/api/v1/transaction/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id: int):
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to get transaction {transaction_id} without valid token')
        raise error.APIAuthError('User is not authorized')

    transaction = Transaction.get(transaction_id=transaction_id, user_id=int(user_id))
    if transaction is None:
        logger.warning(f'User {user_id} is trying to get a non-existent transaction {transaction_id}')
        raise error.APIValueNotFound(f'Transaction {transaction_id} not found')

    logger.info(f'User {user_id} got transaction {transaction_id}')

    return jsonify(formatting(transaction)), 200


@transactions_api.route('/api/v1/transaction/<int:transaction_id>', methods=['PUT'])
@jwt_required()
@jsonbody(type=(int, "required"),
          category=(int, "required"),
          amount=(float, "required"),
          transaction_date=(str, "required"),
          description=(str, None))
def update_transaction(transaction_id: int,
                       type: int,
                       category: int,
                       amount: float,
                       transaction_date: str,
                       description=''):

    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to update transaction {transaction_id} without valid token')
        raise error.APIAuthError('User is not authorized')

    transaction = Transaction.get(transaction_id=transaction_id, user_id=int(user_id))
    if transaction is None:
        logger.warning(f'User {user_id} is trying to update a non-existent transaction {transaction_id}')
        raise error.APIValueNotFound(f'Transaction {transaction_id} not found')

    transactions_type = TransactionType.get(type_id=type)
    if transactions_type is None:
        logger.warning(f'User {user_id} is trying to update transaction with a non-existent type {type}')
        raise error.APIValueNotFound(f'Transaction type with id {type} not found')

    transactions_category = TransactionCategory.get(category_id=category)
    if transactions_category is None:
        logger.warning(f'User {user_id} is trying to update transaction with a non-existent category {category}')
        raise error.APIValueNotFound(f'Transaction category with id {category} not found')

    if amount < 0 or amount > 999999999999:
        logger.warning(f'User {user_id} is trying to create transaction with invalid amount {amount}')
        raise error.APIParamError(f'Amount must be from 0 to 999 999 999 999')

    transaction.type = type
    transaction.category = category
    transaction.amount = amount
    transaction.transaction_date = transaction_date
    transaction.description = description

    db.session.commit()

    logger.info(f'User {user_id} updated transaction {transaction_id}')

    return jsonify(formatting(transaction)), 200


@transactions_api.route('/api/v1/transaction/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id: int):

    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to delete transaction {transaction_id} without valid token')
        raise error.APIAuthError('User is not authorized')

    transaction = Transaction.get(transaction_id=transaction_id, user_id=int(user_id))
    if transaction is None:
        logger.warning(f'User {user_id} is trying to delete a non-existent transaction {transaction_id}')
        raise error.APIValueNotFound(f'Transaction {transaction_id} not found')

    Transaction.delete_transaction(transaction_id=transaction_id)

    logger.info(f'User {user_id} deleted transaction {transaction_id}')

    return jsonify('Ok'), 200
