
from flask import jsonify


class Error:

    def __init__(self, msg, code=None, status=200, data=None):
        self.code = code
        self.status = status
        self.data = data or {}
        self.message = msg
        self.response = None

    def make(self):
        self.response = jsonify({
            'status': self.status,
            'error_code': self.code,
            'message': self.message
        })
        self.response.status_code = self.status
        return self.response


NotFoundError = Error("Not found", "not-found", 404)
BadParams = Error("Bad params", "bad-params", 400)
Unauthorized = Error("Unauthorized", "unauthorized", 401)
Forbidden = Error("Forbidden", "forbidden", 403)
Conflict = Error("Conflict", "conflict", 409)
MethodNotAllowed = Error("Method not allowed", "method-not-allowed", 405)
InternalServerError = Error("Internal server error", "internal-server-error", 500)
NotModified = Error("Not Modified", "not-modyfied", 304)
TooManyRequests = Error("Too Many Requests", "too-many-requests", 429)
def NotRequiredParam(msg): return Error(msg, "bad-params", 400)
def InvalidParamType(msg): return Error(msg, "bad-params", 400)
