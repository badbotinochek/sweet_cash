
from flask import request

import api.errors as error


def clear_data(data: dict, **kwargs) -> dict:
    data = {k: data[k] for k, v in kwargs.items()}
    return data


def jsonbody(**kwargs):

    def decorator(func):
        def wrapper_jsonbody():
            if not request.is_json:
                return error.BadParams("Json required")
            for k, v in kwargs.items():
                parameter = request.json.get(k)
                if parameter is None and v[1] == "required":
                    return error.BadParams(f'{k} is required')
                if type(parameter) is not v[0]:
                    return error.BadParams(f'Invalid type for {k}')
            data = clear_data(request.json, **kwargs)
            return func(**data)
        return wrapper_jsonbody

    return decorator


def query_params(**kwargs):

    def decorator(func):
        def wrapper_query_params():
            for k, v in kwargs.items():
                parameter = request.args.get(k)
                if parameter is None and v[1] == "required":
                    return error.BadParams(f'{k} is required')
                if type(parameter) is not v[0]:
                    return error.BadParams(f'Invalid type for {k}')
            params = {a: request.args.get(a) for a in request.args}
            data = clear_data(params, **kwargs)
            return func(**data)
        return wrapper_query_params

    return decorator
