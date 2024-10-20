from ....infra.api.opensearch import OpenSearch
from ....domain.user.model.user_model import *
from ....config.exception import *
import logging as log
import httpx

log.basicConfig(filemode='w', level=log.INFO)


class SearchService:
    def __init__(self, opensearch: OpenSearch):
        self.opensearch = opensearch

    async def send_mentor(
        self,
        body: ProfileDTO
    ):
        try:
            response = self.opensearch.http_client.put(
                f"/profiles/_doc/{body.user_id}", data=body.json())
            if response.status_code == 201:
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
