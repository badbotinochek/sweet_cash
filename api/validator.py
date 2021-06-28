
from flask import request

import api.errors as error


def jsonbody(**kwargs):

    def decorator(func):
        def wrapper():
            if not request.is_json:
                return error.BadParams("Json required")
            for k, v in kwargs.items():
                parameter = request.json.get(k)
                if parameter is None and v[1] == "required":
                    return error.BadParams(f'{k} is required')
                if type(parameter) is not v[0]:
                    return error.BadParams(f'Invalid type for {k}')
            return func()
        return wrapper

    return decorator
