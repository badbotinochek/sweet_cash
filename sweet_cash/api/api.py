
from flask import request, jsonify
import re
from flask_jwt_extended import jwt_required
import logging
from datetime import datetime

from config import Config
from api.models.session import SessionModel
from api.models.transaction import TransactionModel
from api.models.receipt import ReceiptModel
from api.models.event import EventModel
from api.models.event_participants import EventParticipantsModel
from api.models.transaction_category import TransactionCategoryModel
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
            # Checking for json body presence
            if not request.is_json:
                return error.BadParams("Json required")

            # Checking for required parameters and types
            not_founded_required_params = []
            invalid_types_params = []

            for k, v in kwargs.items():
                parameter = request.json.get(k)
                if parameter is None and v['required']:
                    not_founded_required_params.append(k)
                if parameter is not None and type(parameter) is not v['type']:
                    invalid_types_params.append(k)

            if len(not_founded_required_params) > 0:
                return error.BadParams(f'Params {*not_founded_required_params,} required')

            if len(invalid_types_params) > 0:
                return error.BadParams(f'Invalid type for params {*invalid_types_params,}')

            # Converting input parameters into function arguments
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
            # Checking for required parameters and types
            not_founded_required_params = []
            invalid_types_params = []

            for k, v in kwargs.items():
                parameter = request.args.get(k)
                if parameter is None and v['required']:
                    not_founded_required_params.append(k)
                if parameter is not None and type(parameter) is not v['type']:
                    invalid_types_params.append(k)

            if len(not_founded_required_params) > 0:
                return error.BadParams(f'Params {*not_founded_required_params,} required')

            if len(invalid_types_params) > 0:
                return error.BadParams(f'Invalid type for params {*invalid_types_params,}')

            params = {a: request.args.get(a) for a in request.args}

            # Converting input parameters into function arguments
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


def str2datetime(datetime_str: str):
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    except Exception as e:
        raise error.APIParamError(str(e))


def event_participants_decode(data: list) -> dict:
    total = len(data)
    user_role = None
    user_accepted = False
    participants = []

    # Get user role and status
    for participant in data:
        if participant.user_id == getattr(request, "user_id"):
            user_role = participant.role.value
            user_accepted = participant.accepted

    for participant in data:
        if not user_accepted:
            # Add users participant and managers participant for not accepted user
            if participant.role.value == 'Manager' or participant.user_id == getattr(request, "user_id"):
                participants.append(formatting(participant))
        else:
            if participant not in participants:
                participants.append(formatting(participant))

    return {
        "total": total,
        "your_role": user_role,
        "is_accepted": user_accepted,
        "participants": participants
    }


def formatting(data) -> dict:
    try:
        formatted_data = {}
        if isinstance(data, TransactionModel):
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "updated_at": data.updated_at,
                "number": data.number,
                "user_id": data.user_id,
                "event_id": data.event_id,
                "type": data.type.value,
                "category": TransactionCategoryModel.get_name(data.category),
                "amount": data.amount,
                "transaction_date": data.transaction_date,
                "receipt_id": data.receipt_id,
                "description": data.description
            }
        elif isinstance(data, ReceiptModel):
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "external_id": data.external_id,
                "transaction_id": data.transaction_id
            }
        elif isinstance(data, EventModel):
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "updated_at": data.updated_at,
                "name": data.name,
                "start": data.start,
                "end": data.end,
                "description": data.description,
                "participants_info": event_participants_decode(data.get_participants())
            }
        elif isinstance(data, EventParticipantsModel):
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "updated_at": data.updated_at,
                "user_id": data.user_id,
                "role": data.role.value,
                "is_accepted": data.accepted
            }
        elif type(data) is TransactionCategoryModel:
            formatted_data = {
                "id": data.id,
                "created_at": data.created_at,
                "name": data.name,
                "parent_category_id": data.parent_category_id,
                "description": data.description,
            }
            if hasattr(data, 'sub_categories'):
                formatted_data["sub_categories"] = [formatting(item) for item in data.sub_categories]

        return formatted_data
    except Exception as err:
        logger.error(f'Formatting object {data} error {err}')
        raise error.APIError(f'Formatting error')
