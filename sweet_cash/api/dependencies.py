
from api.services.register_user import RegisterUser
from api.services.login_user import LoginUser
from api.services.create_or_update_transaction import CreateOrUpdateTransaction
from api.services.get_transaction import GetTransaction
from api.services.get_transactions import GetTransactions
from api.services.delete_transaction import DeleteTransaction
from api.services.create_receipt_by_qr import CreateReceiptByQr


def register_user_(**kwargs) -> RegisterUser:
    return RegisterUser(**kwargs)


def login_user_(**kwargs) -> LoginUser:
    return LoginUser(**kwargs)


def create_or_update_transaction_(**kwargs) -> CreateOrUpdateTransaction:
    return CreateOrUpdateTransaction(**kwargs)


def get_transaction_(**kwargs) -> GetTransaction:
    return GetTransaction(**kwargs)


def get_transactions_(**kwargs) -> GetTransactions:
    return GetTransactions(**kwargs)


def delete_transaction_(**kwargs) -> DeleteTransaction:
    return DeleteTransaction(**kwargs)


def create_receipt_by_qr_(**kwargs) -> CreateReceiptByQr:
    return CreateReceiptByQr(**kwargs)

