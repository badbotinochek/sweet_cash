from flask import request, jsonify, Blueprint

from api.validator import jsonbody, query_params
from api.models.session import Session
from api.models.transaction import Transaction
from db import db


transactions_api = Blueprint('transactions', __name__)


@transactions_api.route('/api/v1/transaction', methods=['POST'])
@jsonbody(type=(int, "required"),
          category=(int, "required"),
          amount=(float, "required"),
          transaction_date=(str, "required"),
          description=(str, "required"))
def create_transactions(type: int,
                        category: int,
                        amount: float,
                        transaction_date: str,
                        description: str):
    # Get user_id by request token
    if "Authorization" in request.headers:
        user_id = Session.get_user_id(token=request.headers["Authorization"])

        if user_id is not None:
            t = Transaction(type=type,
                            user_id=user_id,
                            category=category,
                            amount=amount,
                            transaction_date=transaction_date,
                            description=description)
            db.session.add(t)
            db.session.commit()

            return jsonify({"id": t.get_id(),
                            "user_id": t.user_id,
                            "type": t.type,
                            "category": t.category,
                            "amount": t.amount,
                            "transaction_date": t.transaction_date,
                            "created_at": t.created_at}), 200
    return jsonify({}), 200


def formatting(t: Transaction) -> dict:
    formatted_transaction = {
        "id": t.id,
        "created_at": t.created_at,
        "type": t.type,
        "category": t.category,
        "amount": t.amount,
        "description": t.description
    }
    return formatted_transaction


@transactions_api.route('/api/v1/transaction/all', methods=['GET'])
@query_params(limit=(str, None),
              offset=(str, None))
def get_transactions(limit=100, offset=0):

    if "Authorization" in request.headers:
        user_id = Session.get_user_id(token=request.headers["Authorization"])

        if user_id is not None:
            transactions = Transaction.get_transactions(user_id=int(user_id), 
                                                        offset=int(offset), 
                                                        limit=int(limit))

            if transactions is not None:
                transactions = [formatting(t) for t in transactions]

                return jsonify(transactions), 200
    return jsonify({}), 200
