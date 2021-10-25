from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
import logging

from api.validator import jsonbody, query_params
from api.models.session import Session
from api.models.transaction_category import TransactionCategory
from db import db

logger = logging.getLogger(name="transactions_category")

transactions_category_api = Blueprint('transactions_category', __name__)


def formatting(t: TransactionCategory) -> dict:
    formatted_transactions_category = {
        "id": t.id,
        "name": t.name,
        "parent_category_id": t.parent_category_id,
        "description": t.description,
        "deleted": t.deleted
    }
    return formatted_transactions_category


@transactions_category_api.route('/api/v1/transactions_category', methods=['POST'])
@jwt_required()
@jsonbody(name=(str, "required"),
          description=(str, "required"),
          parent_category_id=(int, "required"))
def create_transactions_category(name: str,
                                 description: str,
                                 parent_category_id: int):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

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


@transactions_category_api.route('/api/v1/transactions_category/all', methods=['GET'])
@jwt_required()
def get_transactions_categories():
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    transactions_categories = TransactionCategory.get_transactions_categories()

    transactions_categories = [formatting(t) for t in transactions_categories]

    # TODO собрать дерево категорий

    logger.warning(f'User {user_id} got all transactions categories {t.get_id()}')
    return jsonify(transactions_categories), 200


@transactions_category_api.route('/api/v1/transactions_category/<int:transactions_category_id>', methods=['PUT'])
@jwt_required()
@jsonbody(name=(str, "required"),
          description=(str, "required"),
          deleted=(str, "required"),
          parent_category_id=(int, "required"))
def update_transactions_category(transactions_category_id: int,
                                 name: str,
                                 deleted: str,
                                 description: str,
                                 parent_category_id: int):
    # Get user_id by request token
    token = request.headers["Authorization"].split('Bearer ')[1]
    user_id = Session.get_user_id(token=token)

    if user_id is None:
        logger.warning(f'User {user_id} is trying to create transaction type without valid token')
        raise error.APIAuthError('User is not authorized')

    transactions_category = TransactionCategory.get(category_id=transactions_category_id)
    if transactions_category is None:
        logger.warning(f'User {user_id} is trying to update a non-existent transaction category {transaction_type_id}')
        raise error.APIValueNotFound(f'transactions_category {category_id} not found')

    transactions_category.name = name
    transactions_category.description = description
    transactions_category.deleted = deleted
    transactions_category.parent_category_id = parent_category_id

    db.session.commit()

    logger.info(f'User {user_id} updated transaction category {transactions_category_id}')
    return jsonify(formatting(transactions_category)), 200
