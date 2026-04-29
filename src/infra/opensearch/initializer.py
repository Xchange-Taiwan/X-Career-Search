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

    async def sync_mapping(self, index: str, mapping: Dict) -> bool:
        """
        Apply additive mapping changes (new properties) to an existing index.

        OpenSearch's `PUT /<index>/_mapping` accepts new fields without recreating
        the index, but rejects type changes on existing fields. We rely on that:
        deploys that introduce a new field (e.g. `avatar_updated_at`) take effect
        without manual ops; deploys that try to change an existing field's type
        will surface as a logged error and a no-op rather than a silent drift.

        Returns True when the mapping was applied (or no-op-acknowledged), False
        on any unexpected failure.
        """
        try:
            properties = mapping.get("mappings", {}).get("properties")
            if not properties:
                log.info(
                    "[IndexInitializer] no properties to sync for index '%s'.", index
                )
                return True

            response = self.opensearch.http_client.put(
                f"/{index}/_mapping",
                json={"properties": properties},
            )
            if response.status_code in (200, 201):
                log.info(
                    "[IndexInitializer] mapping for '%s' synced successfully.", index
                )
                return True

            log.error(
                "[IndexInitializer] unexpected response syncing mapping for '%s': status=%s body=%s",
                index, response.status_code, response.json(),
            )
            return False

        except Exception as e:
            log.error("[IndexInitializer] failed to sync mapping for '%s': %s", index, e)
            return False
