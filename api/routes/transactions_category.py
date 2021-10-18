from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from api.validator import jsonbody, query_params
from api.models.session import Session
from api.models.transaction_category import TransactionCategory
from db import db

transactions_category_api = Blueprint('transactions_category', __name__)


def formatting(t: TransactionCategory) -> dict:
    formatted_transaction = {
        "id": t.id,
        "name": t.name,
        "parent_category_id": t.parent_category_id,
        "description": t.description,
        "deleted": t.deleted
    }
    return formatted_transaction


@transactions_category_api.route('/api/v1/transactions_category/all', methods=['GET'])
@query_params(limit=(str, None),
              offset=(str, None))
def get_transactions_category(limit=100, offset=0):
    pass
