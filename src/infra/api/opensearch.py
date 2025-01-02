import httpx
import functools
from src.config.exception import *
from src.config.conf import *
from src.router.res.response import *
from src.infra.template.client_response import ClientResponse
import logging as log

log.basicConfig(filemode="w", level=log.INFO)


def check_response_code(method: str, expected_code: int = 200):
    def decorator_check_response_code(func):

        @functools.wraps(func)
        async def wrapper_check_response_code(*args, **kwargs):
            # request params
            function_name: str = func.__name__
            url = kwargs.get("url", args[1] if len(args) > 1 else None)
            params = kwargs.get("params", args[2] if len(args) > 2 else None)
            body = kwargs.get("json", args[2] if len(args) > 2 else None)
            headers = kwargs.get("headers", args[3] if len(args) > 3 else None)

            # response params
            data: Dict = None
            err_msg: str = None

            api_res: ClientResponse = await func(*args, **kwargs)
            status_code = getattr(api_res, "status_code", -1)
            if status_code in expected_code: # (200, 201)
                return api_res

            err_msg = getattr(api_res, "res_json", "Unhandled exception")
            log.error(
                f"service request fail, \n[%s]: %s, \nbody:%s, \nparams:%s, \nheaders:%s, \nstatus_code:%s, \nerr_msg:%s, \n response:%s",
                method, url, body, params, headers, status_code, err_msg, api_res.res_text,
            )
            raise_http_exception_by_status_code(status_code, err_msg, data)

        return wrapper_check_response_code

    return decorator_check_response_code


class OpenSearch:
    def __init__(self):
        # Init opensearch connection
        # sync
        self.http_client = httpx.Client(
            base_url=OPENSERACH_DOMAIN_ENDPOINT,
            headers={"Content-Type": "application/json"},
            auth=(OPENSERACH_USERNAME, OPENSERACH_PASSWORD),
        )
        # async
        # async with httpx.AsyncClient(
        #     base_url=OPENSERACH_DOMAIN_ENDPOINT,
        #     headers={
        #         "Content-Type": "application/json"
        #     },
        #     auth=(OPENSERACH_USERNAME, OPENSERACH_PASSWORD)
        # ) as client:
        #     self.http_client = client

    @check_response_code("post", (201, 200))
    async def post(
        self, url: str, json: Dict, params: Dict = None, headers: Dict = None
    ) -> Optional[ClientResponse]:
        result = None
        response = None
        try:
            response: httpx.Response = self.http_client.post(
                url, json=json, params=params, headers=headers
            )
            result = ClientResponse.parse(response)

        except httpx.RequestError as e:
            log.error(
                f"[POST] request error, url:%s, json:%s, headers:%s, resp:%s, err:%s",
                url, json, headers, response, e.__str__(),
            )
            raise ClientException(
                msg=f"Request failed: {str(e)}",
            )

        except httpx.HTTPStatusError as e:
            log.error(
                f"[POST] request error, url:%s, json:%s, headers:%s, resp:%s, err:%s",
                url, json, headers, response, e.response.text,
            )
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )

        except Exception as e:
            log.error(
                f"[POST] request error, url:%s, json:%s, headers:%s, resp:%s, err:%s",
                url, json, headers, response, e.__str__(),
            )
            err_msg = getattr(e, "msg", "Unhandled exception")
            raise raise_http_exception(e=e, msg=err_msg)

        return result

    @check_response_code("get", (201, 200))
    async def get(
        self, url: str, params: Dict = None, headers: Dict = None
    ) -> Optional[ClientResponse]:
        result = None
        response = None
        try:
            response: httpx.Response = self.http_client.get(
                url, params=params, headers=headers
            )
            result = ClientResponse.parse(response)

        except httpx.RequestError as e:
            log.error(
                f"[GET] request error, url:%s, params:%s, headers:%s, resp:%s, err:%s",
                url, params, headers, response, e.__str__(),
            )
            raise ClientException(
                msg=f"Request failed: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            log.error(
                f"[GET] request error, url:%s, params:%s, headers:%s, resp:%s, err:%s",
                url, params, headers, response, e.response.text,
            )
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )
        except Exception as e:
            log.error(
                f"[GET] request error, url:%s, params:%s, headers:%s, resp:%s, err:%s",
                url, params, headers, response, e.__str__(),
            )
            err_msg = getattr(e, "msg", "Unhandled exception")
            raise raise_http_exception(e=e, msg=err_msg)

        return result

    @check_response_code("put", (201, 200))
    async def put(
        self, url: str, json: Dict = None, headers: Dict = None
    ) -> Optional[ClientResponse]:
        result = None
        response = None
        try:
            response: httpx.Response = self.http_client.put(
                url, json=json, headers=headers
            )
            result = ClientResponse.parse(response)
        except httpx.RequestError as e:
            log.error(
                f"[PUT] request error, url:%s, json:%s, headers:%s, resp:%s, err:%s",
                url, json, headers, response, e.__str__(),
            )
            raise ClientException(
                msg=f"Request failed: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            log.error(
                f"[PUT] request error, url:%s, json:%s, headers:%s, resp:%s, err:%s",
                url, json, headers, response, e.response.text,
            )
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )
        except Exception as e:
            log.error(
                f"[PUT] request error, url:%s, json:%s, headers:%s, resp:%s, err:%s",
                url, json, headers, response, e.__str__(),
            )
            err_msg = getattr(e, "msg", "Unhandled exception")
            raise raise_http_exception(e=e, msg=err_msg)

        return result

    @check_response_code("delete", (201, 200))
    async def delete(
        self, url: str, params: Dict = None, headers: Dict = None
    ) -> Optional[ClientResponse]:
        result = None
        response = None
        try:
            response: httpx.Response = self.http_client.delete(
                url, params=params, headers=headers
            )
            result = ClientResponse.parse(response)

        except httpx.RequestError as e:
            log.error(
                f"[DELETE] request error, url:%s, params:%s, headers:%s, resp:%s, err:%s",
                url, params, headers, response, e.__str__(),
            )
            raise ClientException(
                msg=f"Request failed: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            log.error(
                f"[DELETE] request error, url:%s, params:%s, headers:%s, resp:%s, err:%s",
                url, params, headers, response, e.response.text,
            )
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )
        except Exception as e:
            log.error(
                f"[DELETE] request error, url:%s, params:%s, headers:%s, resp:%s, err:%s",
                url, params, headers, response, e.__str__(),
            )
            err_msg = getattr(e, "msg", "Unhandled exception")
            raise raise_http_exception(e=e, msg=err_msg)

        return result
