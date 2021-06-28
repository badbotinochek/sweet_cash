
from flask import request

import api.errors as error


def jsonbody(**kwargs):

    def decorator(func):
        def wrapper():
            if not request.is_json:
                return error.BadParams.make()
            for k, v in kwargs.items():
                parameter = request.json.get(k)
                if parameter is None and v[1] == "required":
                    return error.NotRequiredParam(f'{k} is required').make()
                if type(parameter) is not v[0]:
                    return error.InvalidParamType(f'Invalid type for {k}').make()
            return func()
        return wrapper

    return decorator
