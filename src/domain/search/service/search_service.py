from datetime import datetime, timezone
from typing import Callable, Dict

from ....infra.api.opensearch import OpenSearch
from ....domain.mentor.model.mentor_model import MentorProfileDTO
from ....domain.search.model.search_model import SearchMentorProfileDTO
from ....config.constant import MentorAction
from ....config.exception import ClientException
from ....config.conf import PROFILE_STR_DEFAULT_FIELDS
from ....infra.template.client_response import ClientResponse
import logging

log = logging.getLogger(__name__)


class SearchService:
    def __init__(self, opensearch: OpenSearch):
        self.opensearch = opensearch
        self._command_registry: Dict[MentorAction, Callable] = {
            MentorAction.UPSERT_MENTOR_PROFILE: self._upsert_mentor,
            MentorAction.PUT_MENTOR_PROFILE:    self._put_mentor,
            MentorAction.PATCH_MENTOR_PROFILE:  self._patch_mentor_experiences,
            MentorAction.DELETE_MENTOR_PROFILE: self._delete_mentor_by_event,
        }

    # ── SQS consumer entry-point ──────────────────────────────────────────────

    async def subscribe_mentor_update(self, event: Dict):
        ack = event.pop("ack", None)
        action_raw = event.pop("action", MentorAction.UPSERT_MENTOR_PROFILE.value)
        try:
            action = MentorAction(action_raw)
        except ValueError:
            log.warning(
                "[SearchService] unknown action '%s' – falling back to UPSERT.", action_raw
            )
            action = MentorAction.UPSERT_MENTOR_PROFILE

        handler = self._command_registry.get(action)
        if handler:
            await handler(event)
        else:
            log.error("[SearchService] no handler registered for action '%s'.", action)

        if ack:
            await ack()

    # ── Command handlers ──────────────────────────────────────────────────────

    async def _upsert_mentor(self, event: Dict):
        """Full create-or-replace of the mentor profile document."""
        body = MentorProfileDTO(**event)
        await self.send_mentor(body)

    async def _put_mentor(self, event: Dict):
        """Update mentor-specific fields (personal_statement, about, seniority_level,
        expertises).  Uses the same _update + doc_as_upsert path so OpenSearch merges
        only the supplied fields."""
        body = MentorProfileDTO(**event)
        await self.send_mentor(body)

    async def _patch_mentor_experiences(self, event: Dict):
        """Partial update: replace only the `experiences` nested array and bump
        updated_at.  Does NOT touch any other profile fields."""
        user_id = event.get("user_id")
        experiences = event.get("experiences", [])
        now_iso = datetime.now(timezone.utc).isoformat()
        patch_body = {
            "doc": {
                "experiences": experiences,
                "updated_at": now_iso,
            }
        }
        response: ClientResponse = await self.opensearch.post(
            f"/profiles/_update/{user_id}", json=patch_body
        )
        # Mirror the same patch into v2 — best-effort. Don't fail the SQS
        # callback if v2 is missing the doc (alias swap in #233).
        try:
            await self.opensearch.post(
                f"/profiles_v2/_update/{user_id}", json=patch_body
            )
        except Exception as e:
            log.warning("[SearchService] v2 patch failed for user %s: %s", user_id, e)
        return response.res_json

    async def _delete_mentor_by_event(self, event: Dict):
        """Hard-delete the mentor profile document from the index."""
        user_id = event.get("user_id")
        await self.delete_mentor(user_id)

    # ── Core OpenSearch operations ────────────────────────────────────────────

    async def send_mentor(self, body: MentorProfileDTO):
        """Upsert a full mentor profile document into v1 (`profiles`) and the
        v2 unified-tag index (`profiles_v2`).

        v1 doc shape is unchanged. v2 doc carries `user_tags` (when the SQS
        payload includes them) instead of the per-kind nested arrays. Both
        writes use `doc_as_upsert` so the doc is created on first message.
        """
        user_id = body.user_id
        body.updated_at = datetime.now(timezone.utc)
        json_doc = body.to_json()

        # v1 — strip user_tags, keep legacy nested fields
        v1_doc = {k: v for k, v in json_doc.items() if k != "user_tags"}
        v1_response: ClientResponse = await self.opensearch.post(
            f"/profiles/_update/{user_id}",
            json={"doc": v1_doc, "doc_as_upsert": True},
        )

        # v2 — strip legacy per-kind nested arrays, keep user_tags. Once the
        # User-side publisher emits user_tags in every SQS payload (planned
        # follow-up), v2 docs become authoritative.
        v2_legacy_keys = {"interested_positions", "skills", "topics", "expertises"}
        v2_doc = {k: v for k, v in json_doc.items() if k not in v2_legacy_keys}
        try:
            await self.opensearch.post(
                f"/profiles_v2/_update/{user_id}",
                json={"doc": v2_doc, "doc_as_upsert": True},
            )
        except Exception as e:
            log.warning("[SearchService] v2 upsert failed for user %s: %s", user_id, e)

        return v1_response.res_json

    async def delete_mentor(self, user_id: int):
        response: ClientResponse = await self.opensearch.delete(
            f"/profiles/_doc/{user_id}"
        )
        try:
            await self.opensearch.delete(f"/profiles_v2/_doc/{user_id}")
        except Exception as e:
            log.warning("[SearchService] v2 delete failed for user %s: %s", user_id, e)
        return response.res_json

    async def get_mentor_list(self, query: SearchMentorProfileDTO, index: str = "profiles"):
        if query is None:
            raise ClientException(msg="Query could not be None")
        response: ClientResponse = await self.opensearch.post(
            f"/{index}/_search",
            params={"request_cache": "true", "pretty": "true"},
            json=query,
        )
        data = response.res_json
        hits = data.get("hits", {}).get("hits", [])
        mentors = []
        for hit in hits:
            source = hit["_source"]
            [source.setdefault(f, "") for f in PROFILE_STR_DEFAULT_FIELDS]
            mentors.append(source)
        return {"mentors": mentors, "next_id": None}

    async def get_mentor(self, user_id: int):
        # #226: read from profiles_v2 so callers see the new user_tags array
        # (with parent_subject_group). v1 (`profiles`) still receives writes
        # via dual-write for rollback safety, but is no longer the read path
        # for single-mentor lookups.
        response: ClientResponse = await self.opensearch.get(
            f"/profiles_v2/_doc/{user_id}", params={"pretty": "true"}
        )
        data = response.res_json
        source = data.get("_source", {})
        [source.setdefault(f, "") for f in PROFILE_STR_DEFAULT_FIELDS]
        return source
