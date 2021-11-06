from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
import logging

from api.api import jsonbody, query_params, features
from api.models.session import SessionModel
from api.models.transaction_type import TransactionType
from db import db
import api.errors as error

logger = logging.getLogger(name="transaction_types")

transaction_types_api = Blueprint('transaction_types', __name__)


def formatting(t: TransactionType) -> dict:
    formatted_type = {
        "id": t.id,
        "name": t.name,
        "description": t.description
    }
    return formatted_type


@transaction_types_api.route('/api/v1/transaction_type', methods=['POST'])
@jwt_required()
@jsonbody(name=features(type=str, required=True),
          description=features(type=str))
def create_transactions(name: str,
                        description=None):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = SessionModel.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    if description is None:
        t = TransactionType(name=name)
    else:
        t = TransactionType(name=name,
                            description=description)

    db.session.add(t)
    db.session.commit()

    logger.warning(f'User {user_id} created transaction type {t.get_id()}')
    return jsonify(formatting(t)), 200


@transaction_types_api.route('/api/v1/transactions_types', methods=['GET'])
@jwt_required()
@query_params(limit=features(type=str),
              offset=features(type=str))
def get_transactions_types(limit=100, offset=0):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = SessionModel.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to get all transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    transactions_types = TransactionType.get_transaction_types(limit=int(limit),
                                                               offset=int(offset))

    transactions_types = [formatting(t) for t in transactions_types]

    logger.warning(f'User {user_id} got transactions types')
    return jsonify(transactions_types), 200


@transaction_types_api.route('/api/v1/transaction_type/<int:transaction_type_id>', methods=['PUT'])
@jwt_required()
@jsonbody(name=features(type=str, required=True),
          description=features(type=str))
def update_transaction_type(transaction_type_id: int,
                            name: str,
                            description=None):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = SessionModel.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to update transaction {transaction_type_id} type without valid token')
        raise error.APIAuthError('User is not authorized')

    transaction_type = TransactionType.get(type_id=transaction_type_id)
    if transaction_type is None:
        logger.warning(f'User {user_id} is trying to update a non-existent transaction type {transaction_type_id}')
        raise error.APIValueNotFound(f'Transaction type {transaction_type_id} not found')

    transaction_type.name = name
    if description is not None:
        transaction_type.description = description

    db.session.commit()

    logger.info(f'User {user_id} updated transaction type {transaction_type_id}')
    return jsonify(formatting(transaction_type)), 200