
from flask import jsonify, Blueprint


blueprint = Blueprint('error_handlers', __name__)


class APIError(Exception):
    """All custom API Exceptions"""
    code = 500
    description = "Something's wrong"


class APIAuthError(APIError):
    """Custom Authentication Error Class."""
    code = 403
    description = "Authentication Error"


class APIParamError(APIError):
    """Custom Request Parameters Error Class."""
    code = 400
    description = "Request parameters error"


class APIValueNotFound(APIError):
    """Custom Request Parameters Error Class."""
    code = 404
    description = "Not found"


class APIConflict(APIError):
    """Custom Request Parameters Error Class."""
    code = 409
    description = "Conflict"


@blueprint.app_errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    error_code = err.code
    if len(err.args) > 0:
        response["message"] = err.args[0]
    if len(err.args) > 1:
        error_code = err.args[1]
    return jsonify(response), error_code


class Error(object):

    def __init__(self, msg, code=None, status=200, data=None):
        self.code = code
        self.status = status
        self.data = data or {}
        self.message = msg
        self.response = None

    @classmethod
    def make(cls, cmessage=None, ccode=None, cstatus=None):
        class Error(cls):
            def __init__(self, message=None, code=None, status=None, data=None):
                cls.__init__(
                    self, message or cmessage, code or ccode, status or cstatus, data
                )

        return Error

    def __call__(self, environ, start_response):
        self.response = jsonify({
            'status': self.status,
            'error_code': self.code,
            'message': self.message
        })
        self.response.status_code = self.status
        return self.response(environ, start_response)


NotFoundError = Error.make("Not found", "not-found", 404)
BadParams = Error.make("Bad params", "bad-params", 400)
Unauthorized = Error.make("Unauthorized", "unauthorized", 401)
Forbidden = Error.make("Forbidden", "forbidden", 403)
Conflict = Error.make("Conflict", "conflict", 409)
MethodNotAllowed = Error.make("Method not allowed", "method-not-allowed", 405)
InternalServerError = Error.make("Internal server error", "internal-server-error", 500)
NotModified = Error.make("Not Modified", "not-modyfied", 304)
TooManyRequests = Error.make("Too Many Requests", "too-many-requests", 429)
