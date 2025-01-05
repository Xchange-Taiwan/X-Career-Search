from ...domain.search.model.search_model import *


def format_search_mentors_query(
    query: SearchMentorProfileDTO
):

    # Initialize the base query body
    query_body = {
        "query": {
            "bool": {
                "must": []
            }
        }
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

    if query.search_pattern:
        query_body["query"]["bool"]["must"].append({
            "query_string": {
                "query": f"*{query.search_pattern}*"
            }
        })

    # Check if there are any filters added
    if not query_body["query"]["bool"]["must"]:
        # or use an empty query like { "query": { "match_all": {} } }
        query_body = None

    return query_body
