from typing import Dict, List

from src.infra.api.opensearch import OpenSearch
import logging

log = logging.getLogger(__name__)


def _expected_nested_field_names(mapping: Dict) -> List[str]:
    props = mapping.get("mappings", {}).get("properties", {}) or {}
    return [name for name, spec in props.items() if (spec or {}).get("type") == "nested"]


class IndexInitializer:
    def __init__(self, opensearch: OpenSearch):
        self.opensearch = opensearch

    def _warn_if_mapping_mismatch(self, index: str, mapping: Dict) -> None:
        """
        If the index already existed with an older dynamic mapping (e.g. `interested_positions`
        as `text`), writes with nested objects fail with document_parsing_exception. Field types
        cannot be changed in place; operators must reindex or delete and recreate the index.
        """
        expected_nested = set(_expected_nested_field_names(mapping))
        if not expected_nested:
            return
        try:
            response = self.opensearch.http_client.get(f"/{index}/_mapping")
            if response.status_code != 200:
                return
            body = response.json()
            idx_entry = body.get(index, {}) or {}
            props = idx_entry.get("mappings", {}).get("properties", {}) or {}
            for field in sorted(expected_nested):
                spec = props.get(field) or {}
                actual = spec.get("type")
                if actual is None:
                    continue
                if actual != "nested":
                    log.error(
                        "[IndexInitializer] index '%s': field '%s' is mapped as '%s' but "
                        "this service expects 'nested'. OpenSearch cannot convert types in place; "
                        "create a new index using the app mapping, reindex documents, switch alias "
                        "(or delete '%s' and let startup recreate it — data loss — then backfill).",
                        index,
                        field,
                        actual,
                        index,
                    )
        except Exception as e:
            log.warning(
                "[IndexInitializer] could not verify OpenSearch mapping for '%s': %s",
                index,
                e,
            )

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
                self._warn_if_mapping_mismatch(index, mapping)
                return False

            log.error(
                "[IndexInitializer] unexpected response creating index '%s': status=%s body=%s",
                index, response.status_code, body,
            )
            return False

        except Exception as e:
            log.error("[IndexInitializer] failed to ensure index '%s': %s", index, e)
            return False
