from ....infra.api.opensearch import OpenSearch
from ....domain.mentor.model.mentor_model import *
from ....domain.search.model.search_model import *
from ....config.exception import *
from ....infra.template.client_response import ClientResponse
import httpx
import logging as log

log.basicConfig(filemode="w", level=log.INFO)


class SearchService:
    def __init__(self, opensearch: OpenSearch):
        self.opensearch = opensearch

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
        body = MentorProfileDTO(**event)
        res = await self.send_mentor(body)
        if ack:
            await ack()

    async def send_mentor(self, body: MentorProfileDTO):
        user_id = body.user_id
        json_doc = body.to_json()
        upsert_body = {
            "doc": json_doc,
            "doc_as_upsert": True  # 如果文档不存在则创建
        }
        response: ClientResponse = await self.opensearch.post(
            f"/profiles/_update/{user_id}", json=upsert_body
        )
        return response.res_json

    async def delete_mentor(self, user_id: int):
        response: ClientResponse = await self.opensearch.delete(
            f"/profiles/_doc/{user_id}"
        )
        return response.res_json

    async def get_mentor_list(self, query: SearchMentorProfileDTO):
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
