from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any
from ..router.res.response import res_err_format
import logging

log = logging.getLogger(__name__)


class ErrorLogger:
    def __init__(self, msg: str):
        log.error(msg)



class ClientException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '40000', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return self.msg

class UnauthorizedException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '40100', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return self.msg

class ForbiddenException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '40300', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_403_FORBIDDEN

    def __str__(self) -> str:
        return self.msg

class NotFoundException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '40400', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_404_NOT_FOUND

    def __str__(self) -> str:
        return self.msg

class NotAcceptableException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '40600', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE

    def __str__(self) -> str:
        return self.msg

class DuplicateUserException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '40600', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE

    def __str__(self) -> str:
        return self.msg

class TooManyRequestsException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '42900', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_429_TOO_MANY_REQUESTS

    def __str__(self) -> str:
        return self.msg

class ServerException(HTTPException, ErrorLogger):
    def __init__(self, msg: str, code: str = '50000', data: Any = None):
        self.msg = msg
        self.code = code
        self.data = data
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __str__(self) -> str:
        return self.msg


def __client_exception_handler(request: Request, exc: ClientException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __not_acceptable_exception_handler(request: Request, exc: NotAcceptableException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __duplicate_user_exception_handler(request: Request, exc: DuplicateUserException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __too_many_requests_exception_handler(request: Request, exc: TooManyRequestsException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))

def __server_exception_handler(request: Request, exc: ServerException):
    return JSONResponse(status_code=exc.status_code, content=res_err_format(msg=exc.msg, code=exc.code, data=exc.data))




def include_app(app: FastAPI):
    app.add_exception_handler(ClientException, __client_exception_handler)
    app.add_exception_handler(UnauthorizedException, __unauthorized_exception_handler)
    app.add_exception_handler(ForbiddenException, __forbidden_exception_handler)
    app.add_exception_handler(NotFoundException, __not_found_exception_handler)
    app.add_exception_handler(NotAcceptableException, __not_acceptable_exception_handler)
    app.add_exception_handler(DuplicateUserException, __duplicate_user_exception_handler)
    app.add_exception_handler(TooManyRequestsException, __too_many_requests_exception_handler)
    app.add_exception_handler(ServerException, __server_exception_handler)

def raise_http_exception(e: Exception, msg: str = None):
    if isinstance(e, ClientException):
        raise ClientException(msg=msg or e.msg, data=e.data)

    if isinstance(e, UnauthorizedException):
        raise UnauthorizedException(msg=msg or e.msg, data=e.data)

    if isinstance(e, ForbiddenException):
        raise ForbiddenException(msg=msg or e.msg, data=e.data)

    if isinstance(e, NotFoundException):
        raise NotFoundException(msg=msg or e.msg, data=e.data)

    if isinstance(e, NotAcceptableException):
        raise NotAcceptableException(msg=msg or e.msg, data=e.data)

    if isinstance(e, DuplicateUserException):
        raise DuplicateUserException(msg=msg or e.msg, data=e.data)

    if isinstance(e, ServerException):
        raise ServerException(msg=msg or e.msg, data=e.data)

    raise ServerException(msg=msg)

status_code_mapping = {
    400: ClientException,
    401: UnauthorizedException,
    403: ForbiddenException,
    404: NotFoundException,
    406: NotAcceptableException,  # No DuplicateUserException
    429: TooManyRequestsException,
    500: ServerException,
}


def raise_http_exception_by_status_code(status_code: int, msg: Any = None, data: Any = None):
    """ES/OpenSearch 錯誤 body 常為 dict，不可當作 HTTP 回應的 msg 字串。"""
    exc_cls = status_code_mapping.get(status_code)
    if exc_cls is None:
        raise ServerException(
            msg=str(msg) if msg is not None else "error",
            data=data,
        )

    err_text: str
    err_data: Any = data
    if isinstance(msg, str):
        err_text = msg
    else:
        if err_data is None:
            err_data = msg
        if status_code == status.HTTP_404_NOT_FOUND:
            err_text = "Not found"
        elif status_code == status.HTTP_400_BAD_REQUEST:
            err_text = "Bad request"
        elif status_code == status.HTTP_401_UNAUTHORIZED:
            err_text = "Unauthorized"
        elif status_code == status.HTTP_403_FORBIDDEN:
            err_text = "Forbidden"
        else:
            err_text = str(msg)[:1000] if msg is not None else "Error"

    raise exc_cls(msg=err_text, data=err_data)
