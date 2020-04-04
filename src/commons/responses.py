from http import HTTPStatus
from typing import (
    Dict,
    Any,
    Optional,
)

from flask import jsonify


def response_ok(dict_response: Optional[Dict[str, Any]] = None, http_status=HTTPStatus.OK):
    if dict_response:
        response = dict_response
        response['status'] = "OK"
    else:
        response = {
            "status": "OK"
        }

    return jsonify(response), http_status
