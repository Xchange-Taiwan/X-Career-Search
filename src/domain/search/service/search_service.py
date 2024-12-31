from ....infra.api.opensearch import OpenSearch
from ....domain.mentor.model.mentor_model import *
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
                    f"/profiles/_doc/{kwargs.user_id}", json=kwargs.json())
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
            raise ClientException(
                msg=f"Request failed: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )
        except Exception as e:
            raise ServerException(
                msg='Unhandled exception',
            )

    async def send_mentor(
        self,
        body: MentorProfileDTO
    ):
        try:
            user_id = body.user_id
            json_data = body.to_json()
            response = self.opensearch.http_client.put(
                f"/profiles/_doc/{user_id}", json=json_data)
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
            raise ClientException(
                msg=f"Request failed: {str(e)}",
            )
        except httpx.HTTPStatusError as e:
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
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
            raise ClientException(
                msg=f"Request failed: {e}",
            )
        except httpx.HTTPStatusError as e:
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )
        except Exception as e:
            raise ServerException(
                msg=str(e),
            )

    async def get_mentor(
        self, user_id: int
    ):
        try:
            response = self.opensearch.http_client.get(
                f"/profiles/_doc/{user_id}", params={"pretty": "true"})
            if response.status_code in (201, 200):
                data = response.text
                data_object = json.loads(data)['_source']

                return {
                    'status_code': response.status_code,
                    'body': data_object
                }
            else:
                return {
                    'status_code': response.status_code,
                    'body': response.text
                }
        except httpx.RequestError as e:
            raise ClientException(
                msg=f"Request failed: {e}",
            )
        except httpx.HTTPStatusError as e:
            raise ServerException(
                msg=f"HTTP error occurred: {e.response.text}",
            )
        except Exception as e:
            return {
                'error': 'Unhandled exception',
                'message': str(e),
                'status_code': 500
            }
