from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from api.validator import jsonbody, query_params
from api.models.session import Session
from api.models.transaction_type import TransactionType
from db import db

transactions_types_api = Blueprint('transactions_types', __name__)


def formatting(t: TransactionType) -> dict:
    formatted_type = {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "deleted": t.deleted
    }
    return formatted_type


@transactions_types_api.route('/api/v1/transactions_types/all', methods=['GET'])
@jwt_required()
def get_transactions_types():

    transactions_types = TransactionType.get_transactions_types()

    transactions_types = [formatting(t) for t in transactions_types]

    return jsonify(transactions_types), 200


@transactions_types_api.route('/api/v1/transaction_type', methods=['POST'])
@jwt_required()
@jsonbody(name=(str, "required"),
          description=(str, "required"))
def create_transactions(name: str,
                        description: str):

    t = TransactionType(name=name,
                        description=description)
    db.session.add(t)
    db.session.commit()

    return jsonify(formatting(t)), 200


@transactions_types_api.route('/api/v1/transaction_type/<int:transaction_type_id>', methods=['PUT'])
@jwt_required()
@jsonbody(name=(str, "required"),
          description=(str, "required"),
          deleted=(str, "required"))
def update_transaction_type(transaction_type_id: int,
                            name: str,
                            deleted: str,
                            description: str):

    transaction_type = TransactionType.get(type_id=transaction_type_id)
    if transaction_type is None:
        raise error.APIValueNotFound(f'transaction_type {transaction_type_id} not found')

    transaction_type.name = name
    transaction_type.description = description
    transaction_type.deleted = deleted

    db.session.commit()

    return jsonify(formatting(transaction_type)), 200
