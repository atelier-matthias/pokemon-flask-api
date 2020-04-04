from flask import jsonify
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
    MethodNotAllowed,
    Conflict,
    HTTPException,
)


def exception_json_response_parser(exception: HTTPException):
    return jsonify({
        "status": exception.name,
        "code": exception.code
    })


def not_found(exception: NotFound):
    """Page not found."""
    return exception_json_response_parser(exception), exception.code


def bad_request(exception: BadRequest):
    """Bad Request."""
    return exception_json_response_parser(exception), exception.code


def method_not_allowed(exception: MethodNotAllowed):
    """Method Not Allowed."""
    response = jsonify({
        "status": exception.name,
        "code": exception.code,
        "validMethods": exception.valid_methods
    })
    return response, exception.code


def conflict(exception: Conflict):
    """Conflict."""
    response = jsonify({
        "status": exception.name,
        "code": exception.code,
        "details": exception.description
    })
    return response, exception.code


error_handlers_map = {
    400: bad_request,
    404: not_found,
    405: method_not_allowed,
    409: conflict
}
