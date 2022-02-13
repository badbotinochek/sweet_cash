from flask import request, Blueprint
import logging

from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
from api.services.transactions.create_or_update_transaction import CreateOrUpdateTransaction
from api.services.transactions.get_transaction import GetTransaction
from api.services.transactions.get_transactions import GetTransactions
from api.services.transactions.delete_transaction import DeleteTransaction
from api.services.transactions.get_categories import GetCategories

logger = logging.getLogger(name="transactions")

transactions_api = Blueprint('transactions', __name__)


@transactions_api.route('/api/v1/transactions', methods=['POST'])
@auth()
@jsonbody(number=features(type=str, required=True),
          event_id=features(type=int, required=True),
          type=features(type=str, required=True),
          category=features(type=int, required=True),
          amount=features(type=float, required=True),
          transaction_date=features(type=str, required=True),
          receipt_id=features(type=int),
          description=features(type=str))
def create_transaction(number: str,
                       event_id: int,
                       type: str,
                       category: int,
                       amount: float,
                       transaction_date: str,
                       receipt_id=None,
                       description=None,
                       create_or_update_transaction=CreateOrUpdateTransaction()):
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
    result = formatting(create_or_update_transaction(number=number,
                                                     event_id=event_id,
                                                     user_id=getattr(request, "user_id"),
                                                     type=type,
                                                     category_id=category,
                                                     amount=amount,
                                                     transaction_date=transaction_date,
                                                     receipt_id=receipt_id,
                                                     description=description))

    return SuccessResponse(result)


@transactions_api.route('/api/v1/transactions', methods=['GET'])
@auth()
@query_params(limit=features(type=str),
              offset=features(type=str))
def get_transactions(limit=100, offset=0, get_transactions=GetTransactions()):
    transactions = get_transactions(user_id=getattr(request, "user_id"),
                                    limit=limit,
                                    offset=offset)
    result = [formatting(item) for item in transactions]
    return SuccessResponse(result)


@transactions_api.route('/api/v1/transactions/<int:transaction_id>', methods=['GET'])
@auth()
def get_transaction(transaction_id: int, get_transaction=GetTransaction()):
    result = formatting(get_transaction(user_id=getattr(request, "user_id"),
                                        transaction_id=transaction_id))
    return SuccessResponse(result)


@transactions_api.route('/api/v1/transactions/<int:transaction_id>', methods=['PUT'])
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
                       description=None,
                       create_or_update_transaction=CreateOrUpdateTransaction()):
    result = formatting(create_or_update_transaction(user_id=getattr(request, "user_id"),
                                                     transaction_id=transaction_id,
                                                     type=type,
                                                     category_id=category,
                                                     amount=amount,
                                                     transaction_date=transaction_date,
                                                     private=private,
                                                     description=description))
    return SuccessResponse(result)


@transactions_api.route('/api/v1/transactions/<int:transaction_id>', methods=['DELETE'])
@auth()
def delete_transaction(transaction_id: int, delete_transaction=DeleteTransaction()):
    result = delete_transaction(user_id=getattr(request, "user_id"),
                                transaction_id=transaction_id)
    return SuccessResponse(f'{result} transactions deleted')


@transactions_api.route('/api/v1/transactions/categories', methods=['GET'])
@auth()
def get_categories(get_categories=GetCategories()):
    categories = get_categories(user_id=getattr(request, "user_id"))
    result = [formatting(item) for item in categories]
    return SuccessResponse(result)
