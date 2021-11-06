from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
import logging

from api.api import jsonbody, query_params, features
from api.models.session import SessionModel
from api.models.transaction_category import TransactionCategory
from db import db
import api.errors as error

logger = logging.getLogger(name="transaction_categories")

transaction_categories_api = Blueprint('transaction_categories', __name__)


def formatting(t: TransactionCategory) -> dict:
    formatted_transactions_category = {
        "id": t.id,
        "name": t.name,
        "parent_category_id": t.parent_category_id,
        "description": t.description
    }
    return formatted_transactions_category


@transaction_categories_api.route('/api/v1/transactions_category', methods=['POST'])
@jwt_required()
@jsonbody(name=features(type=str, required=True),
          parent_category_id=features(type=int, required=True),
          description=features(type=str))
def create_transactions_category(name: str,
                                 parent_category_id: int,
                                 description='',):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = SessionModel.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    t = TransactionCategory(name=name,
                            description=description,
                            parent_category_id=parent_category_id)
    db.session.add(t)
    db.session.commit()

    logger.warning(f'User {user_id} created transaction category {t.get_id()}')
    return jsonify(formatting(t)), 200


@transaction_categories_api.route('/api/v1/transactions/categories', methods=['GET'])
@jwt_required()
@query_params(limit=features(type=str),
              offset=features(type=str))
def get_transactions_categories(limit=100, offset=0):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = SessionModel.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    transactions_categories = TransactionCategory.get_transaction_categories(limit=int(limit),
                                                                             offset=int(offset))

    transactions_categories = [formatting(t) for t in transactions_categories]
    # TODO собрать дерево категорий

    logger.warning(f'User {user_id} got all transactions categories')
    return jsonify(transactions_categories), 200


@transaction_categories_api.route('/api/v1/transactions_category/<int:transactions_category_id>', methods=['PUT'])
@jwt_required()
@jsonbody(name=features(type=str, required=True),
          parent_category_id=features(type=int),
          description=features(type=str))
def update_transactions_category(transactions_category_id: int,
                                 name: str,
                                 description='',
                                 parent_category_id=-1):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = SessionModel.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    transactions_category = TransactionCategory.get(category_id=transactions_category_id)
    if transactions_category is None:
        logger.warning(f'User {user_id} is trying to update a '
                       f'non-existent transaction category {transactions_category_id}')
        raise error.APIValueNotFound(f'Transaction category {transactions_category_id} not found')

    if description != '':
        transactions_category.description = description

    if parent_category_id != -1:
        transactions_category.parent_category_id = parent_category_id

    transactions_category.name = name
    db.session.commit()

    logger.info(f'User {user_id} updated transaction category {transactions_category_id}')
    return jsonify(formatting(transactions_category)), 200
