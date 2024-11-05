from ....infra.api.opensearch import OpenSearch
from ....domain.user.model.user_model import *
from ....domain.search.model.search_model import *
from ....config.exception import *
import logging as log
import httpx

log.basicConfig(filemode='w', level=log.INFO)


class SearchService:
    def __init__(self, opensearch: OpenSearch):
        self.opensearch = opensearch
    # TODO: Combine Http request with make_request

    async def make_request(self, method: str, **kwargs):
        try:
            if method == 'put':
                response = self.opensearch.http_client.put(
                    f"/profiles/_doc/{kwargs.user_id}", data=kwargs.json())
            if method == 'get':
                response = self.opensearch.http_client.get(
                    f"/profiles/_doc", json=kwargs)
            if response.status_code in (201, 200):
                return response
            else:
                return {
                    'status_code': response.status_code,
                    'body': response.text
                }
        except httpx.RequestError as e:
            return ClientException(
                msg=f"Request failed: {e}"
            )
        except httpx.HTTPStatusError as e:
            return ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
                status=f"{e.response.status_code}"
            )
        except Exception as e:
            return {
                'error': 'Unhandled exception',
                'message': str(e)
            }

    async def send_mentor(
        self,
        body: ProfileDTO
    ):
        try:
            response = self.opensearch.http_client.put(
                f"/profiles/_doc/{body.user_id}", data=body.json())
            if response.status_code in (201, 200):
                return {
                    'status_code': response.status_code,
                    'body': response
                }
            else:
                return {
                    'status_code': response.status_code,
                    'body': response.text
                }
        except httpx.RequestError as e:
            return ClientException(
                msg=f"Request failed: {e}"
            )
        except httpx.HTTPStatusError as e:
            return ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
                status=f"{e.response.status_code}"
            )
        except Exception as e:
            return {
                'error': 'Unhandled exception',
                'message': str(e)
            }

    async def get_mentor_list(
        self, query: SearchMentorProfileDTO
    ):
        try:
            response = self.opensearch.http_client.post(
                f"/profiles/_search", params={"request_cache": "true", "pretty": "true"}, json=query)
            if response.status_code in (201, 200):
                data = response.json()
                hits = data.get('hits', {}).get('hits', [])
                filtered_hits = [hit['_source'] for hit in hits]
                return {
                    'status_code': response.status_code,
                    'body': filtered_hits
                }
            else:
                return {
                    'status_code': response.status_code,
                    'body': response.text
                }
        except httpx.RequestError as e:
            return ClientException(
                msg=f"Request failed: {e}",
                status_code=400
            )
        except httpx.HTTPStatusError as e:
            return ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
                status_code=f"{e.response.status_code}"
            )
        except Exception as e:
            return {
                'error': 'Unhandled exception',
                'message': str(e),
                'status_code': 500
            }
