
from flask import request

import api.errors as error


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
