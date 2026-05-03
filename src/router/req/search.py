from ...domain.search.model.search_model import *


def format_search_mentors_query(query: SearchMentorProfileDTO):
    """Per-bucket filters land on the matching keyword[] field on the root
    document; industry / search_pattern / cursor stay where they were."""
    query_body = {
        "query": {"bool": {"must": [], "filter": []}},
        "sort": [{"updated_at": "asc"}],
        "size": query.limit or PAGE_LIMIT,
    }

    if query.filter_skills:
        query_body["query"]["bool"]["must"].append(
            {"terms": {"want_skill": query.filter_skills}}
        )
    if query.filter_topics:
        query_body["query"]["bool"]["must"].append(
            {"terms": {"want_topic": query.filter_topics}}
        )
    if query.filter_positions:
        query_body["query"]["bool"]["must"].append(
            {"terms": {"want_position": query.filter_positions}}
        )
    if query.filter_expertises:
        # Mentor expertise = HAVE-side skill bucket.
        query_body["query"]["bool"]["must"].append(
            {"terms": {"have_skill": query.filter_expertises}}
        )

    if query.filter_offers:
        # "What I offer" spans both HAVE buckets — match either.
        query_body["query"]["bool"]["must"].append({
            "bool": {
                "should": [
                    {"terms": {"have_skill": query.filter_offers}},
                    {"terms": {"have_topic": query.filter_offers}},
                ],
                "minimum_should_match": 1,
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
