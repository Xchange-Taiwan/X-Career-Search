from typing import Dict
from src.infra.api.opensearch import OpenSearch
import logging

log = logging.getLogger(__name__)


class IndexInitializer:
    def __init__(self, opensearch: OpenSearch):
        self.opensearch = opensearch

    async def ensure_index(self, index: str, mapping: Dict) -> bool:
        """
        Create the OpenSearch index with the given mapping if it does not already exist.

        OpenSearch returns HTTP 400 with error type `resource_already_exists_exception`
        when the index is present; we treat that as a no-op rather than an error.

        Returns True when the index was created, False when it already existed.
        """
        try:
            # Use the underlying sync httpx client directly so we can inspect the
            # raw status code without triggering the raise-on-4xx decorator.
            response = self.opensearch.http_client.put(
                f"/{index}",
                json=mapping,
            )
            if response.status_code in (200, 201):
                log.info("[IndexInitializer] index '%s' created successfully.", index)
                return True

            body = response.json()
            error_type = body.get("error", {}).get("type", "")
            if response.status_code == 400 and error_type == "resource_already_exists_exception":
                log.info("[IndexInitializer] index '%s' already exists – skipping.", index)
                return False

            log.error(
                "[IndexInitializer] unexpected response creating index '%s': status=%s body=%s",
                index, response.status_code, body,
            )
            return False

        except Exception as e:
            log.error("[IndexInitializer] failed to ensure index '%s': %s", index, e)
            return False
