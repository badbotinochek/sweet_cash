
from flask import request, jsonify
import re
from flask_jwt_extended import jwt_required
import logging

from config import Config
from api.models.session import SessionModel
from api.models.transaction import TransactionModel
from api.models.receipt import ReceiptModel
from api.models.transaction_category import TransactionCategory
import api.errors as error


logger = logging.getLogger(name="api")


class SuccessResponse(tuple):

    def __new__(cls, data="Ok", code=200):
        return super(SuccessResponse, cls).__new__(cls, tuple([jsonify(data), code]))


def auth(*args):

    def decorator(func):

        @jwt_required()
        def wrapper(**other_params):
            # Get user_id by request token
            token = request.headers["Authorization"].split('Bearer ')[1]
            user_id = SessionModel.get_user_id(token=token)

            if user_id is None:
                raise error.APIAuthError('User is not authorized')

            setattr(request, "user_id", user_id)

            return func(*args, **other_params)

        # Renaming the function name:
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def features(type, required=False):
    required = required if required is True else False
    return {"type": type, "required": required}


def clear_data(data: dict, **kwargs):
    if data is None:
        return None
    data = {k: data[k] for k, v in kwargs.items() if k in data}
    return data


def jsonbody(*args, **kwargs):

    def decorator(func):
        def wrapper(**other_params):
            if not request.is_json:
                return error.BadParams("Json required")
            for k, v in kwargs.items():
                parameter = request.json.get(k)
                if parameter is None and v['required']:
                    return error.BadParams(f'{k} is required')
                if parameter is not None and type(parameter) is not v['type']:
                    return error.BadParams(f'Invalid type for {k}')
            data = clear_data(request.json, **kwargs)
            data.update(other_params)
            return func(*args, **data)

        # Renaming the function name:
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def query_params(*args, **kwargs):

    def decorator(func):
        def wrapper():
            for k, v in kwargs.items():
                parameter = request.args.get(k)
                if parameter is None and v['required']:
                    return error.BadParams(f'{k} is required')
                if parameter is not None and type(parameter) is not v['type']:
                    return error.BadParams(f'Invalid type for {k}')
            params = {a: request.args.get(a) for a in request.args}
            data = clear_data(params, **kwargs)
            return func(*args, **data)

        # Renaming the function name:
        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def check_email_format(email: str):
    regex = Config.EMAIL_REGEX
    result = re.fullmatch(regex, email)
    return result


def check_phone_format(phone: str):
    regex = Config.PHONE_REGEX
    result = re.fullmatch(regex, phone)
    return result


def check_password_format(password: str):
    regex = Config.PASSWORD_REGEX
    result = re.fullmatch(regex, password)
    return result


def formatting(data) -> dict:
    try:
        formatted_data = {}
        if type(data) is TransactionModel:
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "type": data.type.value,
                "category": TransactionCategory.get_name(data.category),
                "amount": data.amount,
                "transaction_date": data.transaction_date,
                "private": data.private,
                "description": data.description
            }
        elif type(data) is ReceiptModel:
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "external_id": data.external_id,
                "transaction_id": data.transaction_id
            }
        return formatted_data
    except Exception as err:
        logger.error(f'Formatting object {data} error {err}')
        raise error.APIError(f'Formatting error')
