"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException

    
class RefreshException(APIException):
    code = 401
    msg = "refresh token 获取失败"
    error_code = 10100


class Success(APIException):
    code = 201
    msg = "ok"
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1

class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*=^=)!'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class ContentNotSecurity(APIException):
    code = 400
    msg = 'msg is not security'
    error_code = 1008


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1001


class AuthFailed(APIException):
    """授权失败"""
    code = 401
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'