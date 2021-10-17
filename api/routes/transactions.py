from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from api.validator import jsonbody
from api.models.transaction import Transaction
from db import db


transactions_api = Blueprint('transactions', __name__)


@transactions_api.route('/api/v1/transaction', methods=['POST'])
@jwt_required()
@jsonbody(type=(int, "required"),
          category=(int, "required"),
          amount=(float, "required"),
          transaction_date=(str, "required"),
          description=(str, "required"))
def create_transactions():
    transaction_type = request.json.get('type')
    category = request.json.get('category')
    amount = request.json.get('amount')
    transaction_date = request.json.get('transaction_date')
    description = request.json.get('description')

    t = Transaction(type=transaction_type,
                    category=category,
                    amount=amount,
                    transaction_date=transaction_date,
                    description=description)
    db.session.add(t)
    db.session.commit()

    return jsonify({"id": t.get_id()}), 200
