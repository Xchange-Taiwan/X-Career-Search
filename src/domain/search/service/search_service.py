from ....infra.template.service_api import IServiceApi
from ....infra.api.opensearch import OpenSearch
from ....domain.mentor.model.mentor_model import *
from ....domain.search.model.search_model import *
from ....domain.search.model.outbox_message_model import *
from ....config.exception import *
from ....infra.template.client_response import ClientResponse
import logging

log = logging.getLogger(__name__)

POST_OUTBOX_URL = USER_SERVICE_URL + "/v1/internal/outbox/{message_id}"
class SearchService:
    def __init__(self, opensearch: OpenSearch, serviceApi: IServiceApi):
        self.opensearch = opensearch
        self.service_api = serviceApi

    # TODO: Combine Http request with make_request
    async def make_request(self, method: str, **kwargs):
        if method == "put":
            response: ClientResponse = await self.opensearch.http_client.put(
                f"/profiles/_doc/{kwargs.user_id}", json=kwargs.json()
            )
        if method == "get":
            response: ClientResponse = await self.opensearch.http_client.get(
                f"/profiles/_doc", json=kwargs
            )
        return response.res_json

    async def subscribe_mentor_update(self, event: Dict):
        ack = event.pop("ack", None)
        try:
            body = MentorProfileDTO(**event)
            await self.send_mentor(body)
            if ack:
                await ack()
        except Exception as e:
            log.error(f"Failed to process message: {e}")

    async def send_mentor(self, body: MentorProfileDTO):
        user_id = body.user_id
        body.updated_at = datetime.now(timezone.utc)
        json_doc = body.to_json()
        upsert_body = {
            "doc": json_doc,
            "doc_as_upsert": True  # 如果文档不存在则创建
        }
        if body.is_mentor:
            response: ClientResponse = await self.opensearch.post(
                f"/profiles/_update/{user_id}", json=upsert_body
            )

            formatted_url = POST_OUTBOX_URL.format(message_id=body.outbox_id)

            if 200 <= response.status_code < 300:
                log.info("OpenSearch update successful.")

                outbox_payload = OutboxMessageDTO(status=OutboxStatus.SUCCESS)

                await self.service_api.simple_put(
                    url=formatted_url, 
                    json=outbox_payload.model_dump()
                )
            else:
                error_text = await response.text()
                log.error("OpenSearch failed with status %s: %s", response.status, error_text)

                outbox_payload = OutboxMessageDTO(
                    status=OutboxStatus.FAILED,
                    error_msg=f"OpenSearch error: {error_text[:100]}" # restrict the error message length
                )

                await self.service_api.simple_put(
                    url=formatted_url, 
                    json=outbox_payload.model_dump()
                )

            return response.res_json
        else:
            log.info("Skip saving profile to Elasticsearch. is_mentor: %s", body.is_mentor)

    async def delete_mentor(self, user_id: int):
        response: ClientResponse = await self.opensearch.delete(
            f"/profiles/_doc/{user_id}"
        )
        return response.res_json

    async def get_mentor_list(self, query: SearchMentorProfileDTO):
        if query == None:
            raise ClientException(msg="Query could not be None")
        response: ClientResponse = await self.opensearch.post(
            f"/profiles/_search",
            params={"request_cache": "true", "pretty": "true"},
            json=query,
        )
        data = response.res_json
        hits = data.get("hits", {}).get("hits", [])
        filtered_hits = [hit["_source"] for hit in hits]
        return filtered_hits

    async def get_mentor(self, user_id: int):
        response: ClientResponse = await self.opensearch.get(
            f"/profiles/_doc/{user_id}", params={"pretty": "true"}
        )
        data = response.res_json
        return data.get("_source", {})
