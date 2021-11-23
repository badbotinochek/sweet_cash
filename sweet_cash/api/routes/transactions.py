from flask import request, Blueprint
import logging

from api.api import Response, auth, jsonbody, query_params, features
from api.services.transactions import Transaction, formatting

logger = logging.getLogger(name="transactions")

transactions_api = Blueprint('transactions', __name__)


@transactions_api.route('/api/v1/transaction', methods=['POST'])
@auth()
@jsonbody(type=features(type=str, required=True),
          category=features(type=int, required=True),
          amount=features(type=float, required=True),
          transaction_date=features(type=str, required=True),
          private=features(type=bool, required=True),
          description=features(type=str))
def create_transaction(type: str,
                       category: int,
                       amount: float,
                       transaction_date: str,
                       private: bool,
                       description=None):
    """
    Create new user transaction

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
    result = formatting(Transaction(user_id=getattr(request, "user_id"),
                                    type=type,
                                    category_id=category,
                                    amount=amount,
                                    transaction_date=transaction_date,
                                    private=private,
                                    description=description).create_or_update())
    return Response.success(result)


@transactions_api.route('/api/v1/transactions', methods=['GET'])
@auth()
@query_params(limit=features(type=str),
              offset=features(type=str))
def get_transactions(limit=100, offset=0):
    result = Transaction(user_id=getattr(request, "user_id")).get_batch(limit=limit,
                                                                        offset=offset)
    result = [formatting(item) for item in result]
    return Response.success(result)


@transactions_api.route('/api/v1/transaction/<int:transaction_id>', methods=['GET'])
@auth()
def get_transaction(transaction_id: int):
    result = formatting(Transaction(user_id=getattr(request, "user_id"),
                                    transaction_id=transaction_id).get())
    return Response.success(result)


@transactions_api.route('/api/v1/transaction/<int:transaction_id>', methods=['PUT'])
@auth()
@jsonbody(type=features(type=str, required=True),
          category=features(type=int, required=True),
          amount=features(type=float, required=True),
          transaction_date=features(type=str, required=True),
          private=features(type=bool, required=True),
          description=features(type=str))
def update_transaction(transaction_id: int,
                       type: str,
                       category: int,
                       amount: float,
                       transaction_date: str,
                       private: bool,
                       description=None):
    result = formatting(Transaction(user_id=getattr(request, "user_id"),
                                    transaction_id=transaction_id,
                                    type=type,
                                    category_id=category,
                                    amount=amount,
                                    transaction_date=transaction_date,
                                    private=private,
                                    description=description).create_or_update())
    return Response.success(result)


@transactions_api.route('/api/v1/transaction/<int:transaction_id>', methods=['DELETE'])
@auth()
def delete_transaction(transaction_id: int):
    result = Transaction(user_id=getattr(request, "user_id"),
                         transaction_id=transaction_id).delete()
    return Response.success(f'{result} transactions deleted')
