from ...domain.search.model.search_model import *


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
