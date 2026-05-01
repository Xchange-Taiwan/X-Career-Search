from ...domain.search.model.search_model import *


def _add_user_tags_filter(query_body: Dict, kind: str, intent: str, subject_groups: List[str]):
    # Reusable nested user_tags clause for the v2 query builder. Each nested
    # query matches a row in `profiles_v2.user_tags` whose (kind, intent,
    # subject_group) all line up.
    query_body["query"]["bool"]["must"].append({
        "nested": {
            "path": "user_tags",
            "query": {
                "bool": {
                    "must": [
                        {"term": {"user_tags.kind": kind}},
                        {"term": {"user_tags.intent": intent}},
                        {"terms": {"user_tags.subject_group": subject_groups}},
                    ]
                }
            },
        }
    })


def format_search_mentors_query_v2(query: SearchMentorProfileDTO):
    """v2 (#230-#232) query builder. Emits nested `user_tags` queries for
    every per-kind filter (skills/topics/positions/expertises/offers) so the
    Search service can target `profiles_v2`. v1 top-level fields like
    `industry`, plus `search_pattern` and `cursor`, work the same on both
    indices and are reused here."""
    query_body = {
        "query": {"bool": {"must": [], "filter": []}},
        "sort": [{"updated_at": "asc"}],
        "size": query.limit or PAGE_LIMIT,
    }

    if query.filter_skills:
        _add_user_tags_filter(query_body, "skill", "WANT", query.filter_skills)
    if query.filter_topics:
        _add_user_tags_filter(query_body, "topic", "WANT", query.filter_topics)
    if query.filter_positions:
        _add_user_tags_filter(query_body, "position", "WANT", query.filter_positions)
    if query.filter_expertises:
        # Post-#226 kind-consolidation: mentor expertise lives on the same
        # skill tree, distinguished by intent=OFFER. The legacy `expertise`
        # kind was dropped from the User-service TagKind enum.
        _add_user_tags_filter(query_body, "skill", "OFFER", query.filter_expertises)

    if query.filter_offers:
        # `filter_offers` matches mentor offerings — intent=OFFER on either
        # the skill or topic tree. Post-#226 kind consolidation, the legacy
        # `what_i_offer` and `expertise` kinds no longer exist.
        query_body["query"]["bool"]["must"].append({
            "nested": {
                "path": "user_tags",
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"user_tags.intent": "OFFER"}},
                            {"terms": {"user_tags.subject_group": query.filter_offers}},
                        ],
                        "filter": [
                            {"terms": {"user_tags.kind": ["skill", "topic"]}}
                        ],
                    }
                },
            }
        })

    if query.filter_industries:
        query_body["query"]["bool"]["must"].append({
            "query_string": {
                "default_field": "industry",
                "query": f"*{query.filter_industries}*",
            }
        })

    if query.search_pattern:
        query_body["query"]["bool"]["must"].append(
            {"query_string": {"query": f"*{query.search_pattern}*"}}
        )

    if query.cursor:
        query_body["query"]["bool"]["filter"].append(
            {"range": {"updated_at": {"gt": query.cursor.isoformat()}}}
        )

    if (
        not query_body["query"]["bool"]["must"]
        and not query_body["query"]["bool"]["filter"]
    ):
        query_body = {
            "query": {"bool": {"must": []}},
            "sort": [{"updated_at": "asc"}],
            "size": query.limit or 9,
        }

    return query_body


def format_search_mentors_query(
    query: SearchMentorProfileDTO
):

    # Initialize the base query body
    query_body = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        },
        "sort": [
            { "updated_at": "asc" }
        ],
        "size": query.limit or PAGE_LIMIT
    }

    # Conditionally add query_string filters
    if query.filter_positions:
        query_body["query"]["bool"]["must"].append({
            "query_string": {
                "default_field": "interested_positions",
                "query": " AND ".join(query.filter_positions)
            }
        })

    if query.filter_skills:
        query_body["query"]["bool"]["must"].append({
            "query_string": {
                "default_field": "skills",
                "query": " AND ".join(query.filter_skills)
            }
        })

    if query.filter_topics:
        query_body["query"]["bool"]["must"].append({
            "query_string": {
                "default_field": "topics",
                "query": " AND ".join(query.filter_topics)
            }
        })

    if query.filter_expertises:
        query_body["query"]["bool"]["must"].append(
            {
                "query_string": {
                    "default_field": "expertises",
                    "query": " AND ".join(query.filter_expertises),
                }
            }
        )

    if query.filter_industries:
        query_body["query"]["bool"]["must"].append({
            "query_string": {
                "default_field": "industry",
                "query": f"*{query.filter_industries}*"
            }
        })

    # `filter_offers` is now v2-only; this v1 builder is unreachable for it
    # (route forces v2 routing whenever filter_offers is set). Removed in this
    # PR alongside the kind consolidation; the v2 builder is the sole owner.

    if query.search_pattern:
        query_body["query"]["bool"]["must"].append(
            {"query_string": {"query": f"*{query.search_pattern}*"}}
        )

    if query.cursor:
        query_body["query"]["bool"]["filter"].append(
            {"range": {"updated_at": {"gt": query.cursor.isoformat()}}}
        )
        # query_body["search_after"] = [query.cursor, query.last_id]

    # Check if there are any filters added
    if (
        not query_body["query"]["bool"]["must"]
        and not query_body["query"]["bool"]["filter"]
    ):
        # or use an empty query like { "query": { "match_all": {} } }
        # query_body = None
        query_body = {"query": {"bool": {"must": []}}, "sort": [{ "updated_at": "asc" }], "size": query.limit or 9}

    return query_body
